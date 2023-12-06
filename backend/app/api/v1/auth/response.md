## A note about the response

由于 SQLModel 在 exec() 方法执行时，返回类型为 

`TupleResult[_TSelectParam], ScalarResult[_TSelectParam]`

，但是实际返回类型应为 `_RT = TypeVar("_RT", bound="Result[Any]")`

不能确定当前返回类型是否包含 `rowcount` 属性，可以肯定的是 `Result[Any]` 包含此属性

这里并没有对接口进行实验，感兴趣的话可以尝试一下，如果可行，可以统一响应返回接口，

请参考：[fastapi-practices](https://github.com/fastapi-practices) 中其他相关脚手架

如果可行，请注意 crud 中的方法返回类型及返回值
