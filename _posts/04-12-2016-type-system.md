---
layout: post
title: Type system
author: mrexodia
website: http://mrexodia.cf
---

This week there wasn't much going on in the codebase and therefore I decided to skip the weekly digest and write a more substantial post. Hopefully it's an interesting read!

## Internal representation

The internal representation of the types is inspired by the [radare2 type profiles](https://github.com/radare/radare2/blob/20c97cb778d16afbe38377184b684f1cbe64831f/doc/types.md) document by [oddcoder](https://github.com/oddcoder).

### Primitives

```c++
enum Primitive
{
    Void,
    Int8,
    Uint8,
    Int16,
    Uint16,
    Int32,
    Uint32,
    Int64,
    Uint64,
    Dsint,
    Duint,
    Float,
    Double,
    Pointer,
    PtrString, //char* (null-terminated)
    PtrWString //wchar_t* (null-terminated)
};
```

Complex types are built from primitive types (see the full list above). The `Void` primitive is not a real type (it cannot have a value) and it's used as a special case. An alternative name would be `Unknown` but that was already taken.

All primitive types (except `Void`) have a fixed size, but that size is not defined as part of the primitive (abstractions love to be abstract). Notice that there is no `Bit` primitive, which means that bit fields or bit arrays are not supportable in the current type system. There are two primitives to represent the common null-terminated string pointer types, mostly for convenience of the user.

The generic `Pointer` type is equivalent to `void*` and can get a more specific meaning in the `Type` representation below.

### Types

```c++
struct Type
{
    std::string owner; //Type owner
    std::string name; //Type identifier.
    std::string pointto; //Type identifier of *Type
    Primitive primitive; //Primitive type.
    int size = 0; //Size in bytes.
};
```

The actual type representation used to represent a primitive type, in say a `struct` is shown above. The comments should be pretty self-explanatory, but it is worth mentioning that the `size` member cannot be defined by user-types directly. You can create your own (named) types and for that you can use one of the pre-defined internal types:

```c++
p("int8_t,int8,char,byte,bool,signed char", Int8, sizeof(char));
p("uint8_t,uint8,uchar,unsigned char,ubyte", Uint8, sizeof(unsigned char));
p("int16_t,int16,wchar_t,char16_t,short", Int16, sizeof(short));
p("uint16_t,uint16,ushort,unsigned short", Int16, sizeof(unsigned short));
p("int32_t,int32,int,long", Int32, sizeof(int));
p("uint32_t,uint32,unsigned int,unsigned long", Uint32, sizeof(unsigned int));
p("int64_t,int64,long long", Int64, sizeof(long long));
p("uint64_t,uint64,unsigned long long", Uint64, sizeof(unsigned long long));
p("dsint", Dsint, sizeof(void*));
p("duint,size_t", Duint, sizeof(void*));
p("float", Float, sizeof(float));
p("double", Double, sizeof(double));
p("ptr,void*", Pointer, sizeof(void*));
p("char*,const char*", PtrString, sizeof(char*));
p("wchar_t*,const wchar_t*", PtrWString, sizeof(wchar_t*));
```

The `p` function simply binds all (comma-separated) type names to a `Primitive` and a size. The sizes are defined by your compiler implementation.

The `owner` member is used to represent what created the type. This will generally be the filename of the file it was loaded from, or `cmd` if the type was created with the [commands](http://help.x64dbg.com/en/latest/commands/types/index.html).

The `pointto` member is used when `primitive` is `Pointer` and it's the name of the type that the pointer points to. As an example, the type `MyStruct*` will have the following values:

```c++
t.owner = owner; //owner of MyStruct
t.name = "MyStruct*";
t.pointto = "MyStruct";
t.primitive = Pointer;
t.size = sizeof(void*); //predefined
```

The [validPtr](https://github.com/x64dbg/x64dbg/blob/8c1b9ccd3f7ca016dc878e4c0d5ff790d4313feb/src/dbg/types.cpp#L307) function will (recursively) create pointer type aliases if you use a construct like `MyStruct*` as part of checking if a type is defined.

### Members

```c++
struct Member
{
    std::string name; //Member identifier
    std::string type; //Type.name
    int arrsize = 0; //Number of elements if Member is an array
    int offset = -1; //Member offset (only stored for reference)
};
```

If you use a definition inside a complex type (think `struct`) it will use the `Member` representation from above. A member like `int arrsize;` will have the following values:

```c++
m.name = "arrsize";
m.type = "int";
m.arrsize = 0; //not an array
m.offset = -1; //unused, only for reference
```

If the `arrsize` member is bigger than zero it means that the member was an array of fixed size. For instance `bool threadsDone[10];`.

### StructUnions

```c++
struct StructUnion
{
    std::string owner; //StructUnion owner
    std::string name; //StructUnion identifier
    std::vector<Member> members; //StructUnion members
    bool isunion = false; //Is this a union?
    int size = 0;
};
```

The definition of a `struct` (or `union`) shouldn't be very surprising. A `struct` is simply a list of `Member` instances. The `size` member is used in the `Sizeof` function and is the combined size of all members. This means that there is **no implicit alignment**. When adding a member with a defined `offset` it will simply put an array of padding bytes to make up for the missing space. This also means that you cannot define members **out of memory order**. This is to prevent overlapping members and also to prevent lots of complexity that isn't needed for most use cases.

### Functions

```c++
struct Function
{
    std::string owner; //Function owner
    std::string name; //Function identifier
    std::string rettype; //Function return type
    CallingConvention callconv; //Function calling convention
    bool noreturn; //Function does not return (ExitProcess, _exit)
    std::vector<Member> args; //Function arguments
};
```

Functions are similar to structs, but they also have a return type and a calling convention. You can define functions (and their arguments), but they are (currently) not used by the GUI. In the future they can be used to provide argument information.

### Where is the tree?

You might have noticed that the data structures don't have a direct tree structure. The main reason for this is that trees are annoying to both represent and manipulate in C++. They are also annoying to serialize and considering that x64dbg uses JSON as a general format I decided to store everything in dictionaries and leave the trees implicit.

There are dictionaries for the `Type`, `StructUnion` and `Function` structures as described above. The `type` field inside `Member` for example is a key in either of these dictionaries and that is how the tree's edges are represented. The tree nodes are the values in the dictionary.

#### Visitor

```c++
struct Visitor
{
    virtual ~Visitor() { }
    virtual bool visitType(const Member & member, const Type & type) = 0;
    virtual bool visitStructUnion(const Member & member, const StructUnion & type) = 0;
    virtual bool visitArray(const Member & member) = 0;
    virtual bool visitPtr(const Member & member, const Type & type) = 0;
    virtual bool visitBack(const Member & member) = 0;
};
```

The tree structure returns in the `Visitor`. The [visitMember](https://github.com/x64dbg/x64dbg/blob/development/src/dbg/types.cpp#L356) function recursively walks a `Member` and it's subtypes with [depth first search](https://en.wikipedia.org/wiki/Depth-first_search) and it will call one of the `visitX` functions to signal that a certain kind of node was visited. The `visitBack` function is called when a complex type subtree was left.

As an example, take the `Ray` structure:

```c++
struct Vec3
{
    int x;
    int y;
    int z;
};

struct Ray
{
    float speed;
    Vec3 direction;
    int lifetime;
};
```

The tree and the order the nodes are visited in can be visualized like this:

![ray tree](http://i.imgur.com/VqDqQfm.png)

The actual structure view in x64dbg will look like this:

![ray struct](http://i.imgur.com/ta83myi.png)

## Conclusion

This post has mostly highlighted the internal representation of the type system, for more information on how to actually use it in x64dbg you can check out [Weekly Digest 14](http://x64dbg.com/blog/2016/11/27/weekly-digest-14.html#types) and if you have any questions, please leave comments and I will try to address them.