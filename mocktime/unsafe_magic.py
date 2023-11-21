# 《深度剖析CPython解释器》34. 侵入 Python 虚拟机，动态修改底层数据结构和运行时
# https://www.cnblogs.com/traditional/p/15489296.html
# !!! 注意，魔法方法(magic methods)动态修改虽然提供了支持，但要慎用，因为在不同版本中实现可能不同

import gc
from ctypes import *


# 将这些对象提前声明好，之后再进行成员的初始化
class PyObject(Structure):
    pass


class PyTypeObject(Structure):
    pass


class PyNumberMethods(Structure):
    pass


class PySequenceMethods(Structure):
    pass


class PyMappingMethods(Structure):
    pass


class PyAsyncMethods(Structure):
    pass


class PyFile(Structure):
    pass


PyObject._fields_ = [("ob_refcnt", c_ssize_t),
                     ("ob_type", POINTER(PyTypeObject))]

PyTypeObject._fields_ = [
    ('ob_base', PyObject),
    ('ob_size', c_ssize_t),
    ('tp_name', c_char_p),
    ('tp_basicsize', c_ssize_t),
    ('tp_itemsize', c_ssize_t),
    ('tp_dealloc', CFUNCTYPE(None, py_object)),
    ('printfunc', CFUNCTYPE(c_int, py_object, POINTER(PyFile), c_int)),
    ('getattrfunc', CFUNCTYPE(py_object, py_object, c_char_p)),
    ('setattrfunc', CFUNCTYPE(c_int, py_object, c_char_p, py_object)),
    ('tp_as_async', CFUNCTYPE(PyAsyncMethods)),
    ('tp_repr', CFUNCTYPE(py_object, py_object)),
    ('tp_as_number', POINTER(PyNumberMethods)),
    ('tp_as_sequence', POINTER(PySequenceMethods)),
    ('tp_as_mapping', POINTER(PyMappingMethods)),
    ('tp_hash', CFUNCTYPE(c_int64, py_object)),
    ('tp_call', CFUNCTYPE(py_object, py_object, py_object, py_object)),
    ('tp_str', CFUNCTYPE(py_object, py_object)),
    # 不需要的可以不用写
]

# 方法集就是一个结构体实例，结构体成员都是函数
# 所以这里我们要相关的函数类型声明好
inquiry = CFUNCTYPE(c_int, py_object)
unaryfunc = CFUNCTYPE(py_object, py_object)
binaryfunc = CFUNCTYPE(py_object, py_object, py_object)
ternaryfunc = CFUNCTYPE(py_object, py_object, py_object, py_object)
lenfunc = CFUNCTYPE(c_ssize_t, py_object)
ssizeargfunc = CFUNCTYPE(py_object, py_object, c_ssize_t)
ssizeobjargproc = CFUNCTYPE(c_int, py_object, c_ssize_t, py_object)
objobjproc = CFUNCTYPE(c_int, py_object, py_object)
objobjargproc = CFUNCTYPE(c_int, py_object, py_object, py_object)

PyNumberMethods._fields_ = [
    ('nb_add', binaryfunc),
    ('nb_subtract', binaryfunc),
    ('nb_multiply', binaryfunc),
    ('nb_remainder', binaryfunc),
    ('nb_divmod', binaryfunc),
    ('nb_power', ternaryfunc),
    ('nb_negative', unaryfunc),
    ('nb_positive', unaryfunc),
    ('nb_absolute', unaryfunc),
    ('nb_bool', inquiry),
    ('nb_invert', unaryfunc),
    ('nb_lshift', binaryfunc),
    ('nb_rshift', binaryfunc),
    ('nb_and', binaryfunc),
    ('nb_xor', binaryfunc),
    ('nb_or', binaryfunc),
    ('nb_int', unaryfunc),
    ('nb_reserved', c_void_p),
    ('nb_float', unaryfunc),
    ('nb_inplace_add', binaryfunc),
    ('nb_inplace_subtract', binaryfunc),
    ('nb_inplace_multiply', binaryfunc),
    ('nb_inplace_remainder', binaryfunc),
    ('nb_inplace_power', ternaryfunc),
    ('nb_inplace_lshift', binaryfunc),
    ('nb_inplace_rshift', binaryfunc),
    ('nb_inplace_and', binaryfunc),
    ('nb_inplace_xor', binaryfunc),
    ('nb_inplace_or', binaryfunc),
    ('nb_floor_divide', binaryfunc),
    ('nb_true_divide', binaryfunc),
    ('nb_inplace_floor_divide', binaryfunc),
    ('nb_inplace_true_divide', binaryfunc),
    ('nb_index', unaryfunc),
    ('nb_matrix_multiply', binaryfunc),
    ('nb_inplace_matrix_multiply', binaryfunc)]

PySequenceMethods._fields_ = [
    ('sq_length', lenfunc),
    ('sq_concat', binaryfunc),
    ('sq_repeat', ssizeargfunc),
    ('sq_item', ssizeargfunc),
    ('was_sq_slice', c_void_p),
    ('sq_ass_item', ssizeobjargproc),
    ('was_sq_ass_slice', c_void_p),
    ('sq_contains', objobjproc),
    ('sq_inplace_concat', binaryfunc),
    ('sq_inplace_repeat', ssizeargfunc)]

# 将这些魔法方法的名字和底层的结构体成员组合起来
magic_method_dict = {
    "__add__": ("tp_as_number", "nb_add"),
    "__sub__": ("tp_as_number", "nb_subtract"),
    "__mul__": ("tp_as_number", "nb_multiply"),
    "__mod__": ("tp_as_number", "nb_remainder"),
    "__pow__": ("tp_as_number", "nb_power"),
    "__neg__": ("tp_as_number", "nb_negative"),
    "__pos__": ("tp_as_number", "nb_positive"),
    "__abs__": ("tp_as_number", "nb_absolute"),
    "__bool__": ("tp_as_number", "nb_bool"),
    "__inv__": ("tp_as_number", "nb_invert"),
    "__invert__": ("tp_as_number", "nb_invert"),
    "__lshift__": ("tp_as_number", "nb_lshift"),
    "__rshift__": ("tp_as_number", "nb_rshift"),
    "__and__": ("tp_as_number", "nb_and"),
    "__xor__": ("tp_as_number", "nb_xor"),
    "__or__": ("tp_as_number", "nb_or"),
    "__int__": ("tp_as_number", "nb_int"),
    "__float__": ("tp_as_number", "nb_float"),
    "__iadd__": ("tp_as_number", "nb_inplace_add"),
    "__isub__": ("tp_as_number", "nb_inplace_subtract"),
    "__imul__": ("tp_as_number", "nb_inplace_multiply"),
    "__imod__": ("tp_as_number", "nb_inplace_remainder"),
    "__ipow__": ("tp_as_number", "nb_inplace_power"),
    "__ilshift__": ("tp_as_number", "nb_inplace_lshift"),
    "__irshift__": ("tp_as_number", "nb_inplace_rshift"),
    "__iand__": ("tp_as_number", "nb_inplace_and"),
    "__ixor__": ("tp_as_number", "nb_inplace_xor"),
    "__ior__": ("tp_as_number", "nb_inplace_or"),
    "__floordiv__": ("tp_as_number", "nb_floor_divide"),
    "__div__": ("tp_as_number", "nb_true_divide"),
    "__ifloordiv__": ("tp_as_number", "nb_inplace_floor_divide"),
    "__idiv__": ("tp_as_number", "nb_inplace_true_divide"),
    "__index__": ("tp_as_number", "nb_index"),
    "__matmul__": ("tp_as_number", "nb_matrix_multiply"),
    "__imatmul__": ("tp_as_number", "nb_inplace_matrix_multiply"),

    "__len__": ("tp_as_sequence", "sq_length"),
    "__concat__": ("tp_as_sequence", "sq_concat"),
    "__repeat__": ("tp_as_sequence", "sq_repeat"),
    "__getitem__": ("tp_as_sequence", "sq_item"),
    "__setitem__": ("tp_as_sequence", "sq_ass_item"),
    "__contains__": ("tp_as_sequence", "sq_contains"),
    "__iconcat__": ("tp_as_sequence", "sq_inplace_concat"),
    "__irepeat__": ("tp_as_sequence", "sq_inplace_repeat")
}

keep_method_alive = {}
keep_method_set_alive = {}


# 以上就准备就绪了，下面再将之前的 patch_builtin_class 函数补充一下即可
def patch_builtin_class(cls, name, value):
    """
    :param cls: 要修改的类
    :param name: 属性名或者函数名
    :param value: 值
    :return:
    """
    if type(cls) is not type:
        raise ValueError("cls 必须是一个内置的类对象")
    cls_attrs = gc.get_referents(cls.__dict__)[0]
    old_value = cls_attrs.get(name, None)
    cls_attrs[name] = value
    if old_value is not None:
        try:
            value.__name__ = old_value.__name__
            value.__qualname__ = old_value.__qualname__
        except AttributeError:
            pass
        cls_attrs[f"_{cls.__name__}_{name}"] = old_value
    pythonapi.PyType_Modified(py_object(cls))
    # 以上逻辑不变，然后对参数 name 进行检测
    # 如果是魔方方法、并且 value 是一个可调用对象，那么修改操作符，否则直接 return
    if name not in magic_method_dict and callable(value):
        return
    # 比如 name 是 __sub__，那么 tp_as_name, rewrite == "tp_as_number", "nb_sub"
    tp_as_name, rewrite = magic_method_dict[name]
    # 获取类对应的底层结构，PyTypeObject 实例
    type_obj = PyTypeObject.from_address(id(cls))
    # 根据 tp_as_name 判断到底是哪一个方法集，这里我们没有实现 tp_as_mapping 和 tp_as_async
    struct_method_set_class = (PyNumberMethods if tp_as_name == "tp_as_number"
                               else PySequenceMethods if tp_as_name == "tp_as_sequence"
    else PyMappingMethods if tp_as_name == "tp_as_mapping"
    else PyAsyncMethods)
    # 获取具体的方法集（指针）
    struct_method_set_ptr = getattr(type_obj, tp_as_name, None)
    if not struct_method_set_ptr:
        # 如果不存在此方法集，我们实例化一个，然后设置到里面去
        struct_method_set = struct_method_set_class()
        # 注意我们要传一个指针进去
        setattr(type_obj, tp_as_name, pointer(struct_method_set))
    # 然后对指针进行解引用，获取方法集，也就是对应的结构体实例
    struct_method_set = struct_method_set_ptr.contents
    # 遍历 struct_method_set_class，判断到底重写的是哪一个魔法方法
    cfunc_type = None
    for field, ftype in struct_method_set_class._fields_:
        if field == rewrite:
            cfunc_type = ftype
    # 构造新的函数
    cfunc = cfunc_type(value)
    # 更新方法集
    setattr(struct_method_set, rewrite, cfunc)
    # 至此我们的功能就完成了，但还有一个非常重要的点，就是上面的 cfunc
    # 虽然它是一个底层可以识别的 C 函数，但它本质上仍然是一个 Python 对象
    # 其内部维护了 C 级数据，赋值之后底层会自动提取，而这一步不会增加引用计数
    # 所以这个函数结束之后，cfunc 就被销毁了（连同内部的 C 级数据）
    # 这样后续再调用相关操作符的时候就会出现段错误，解释器异常退出
    # 因此我们需要在函数结束之前创建一个在外部持有它的引用
    keep_method_alive[(cls, name)] = cfunc
    # 当然还有我们上面的方法集，也是同理
    keep_method_set_alive[(cls, name)] = struct_method_set
