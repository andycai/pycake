from convert import *

def test_convert():
    # 测试整数转换
    print("整数转换测试:")
    print(f"to_int('123') = {to_int('123')}")
    print(f"to_int('abc', 0) = {to_int('abc', 0)}")
    print()

    # 测试浮点数转换
    print("浮点数转换测试:")
    print(f"to_float('3.14') = {to_float('3.14')}")
    print(f"to_float('abc', 0.0) = {to_float('abc', 0.0)}")
    print()

    # 测试布尔值转换
    print("布尔值转换测试:")
    print(f"to_bool('true') = {to_bool('true')}")
    print(f"to_bool('false') = {to_bool('false')}")
    print(f"to_bool('1') = {to_bool('1')}")
    print(f"to_bool('0') = {to_bool('0')}")
    print()

    # 测试日期时间转换
    print("日期时间转换测试:")
    print(f"to_datetime('2024-03-20 15:30:00') = {to_datetime('2024-03-20 15:30:00')}")
    print(f"to_date('2024-03-20') = {to_date('2024-03-20')}")
    print(f"to_time('15:30:00') = {to_time('15:30:00')}")
    print()

    # 测试列表转换
    print("列表转换测试:")
    print(f"to_list('1,2,3,4,5') = {to_list('1,2,3,4,5')}")
    print(f"to_list('1,2,3,4,5', converter='int') = {to_list('1,2,3,4,5', converter='int')}")
    print(f"to_list('1.1,2.2,3.3', converter='float') = {to_list('1.1,2.2,3.3', converter='float')}")
    print(f"to_list('true,false,1,0', converter='bool') = {to_list('true,false,1,0', converter='bool')}")
    print()

    # 测试字典转换
    print("字典转换测试:")
    print(f"to_dict('a:1,b:2,c:3') = {to_dict('a:1,b:2,c:3')}")
    print(f"to_dict('a:1,b:2,c:3', converter='int') = {to_dict('a:1,b:2,c:3', converter='int')}")
    print(f"to_dict('a:1.1,b:2.2,c:3.3', converter='float') = {to_dict('a:1.1,b:2.2,c:3.3', converter='float')}")
    print(f"to_dict('a:true,b:false,c:1', converter='bool') = {to_dict('a:true,b:false,c:1', converter='bool')}")
    print()

    # 测试进制转换
    print("进制转换测试:")
    print(f"to_hex('0xFF') = {to_hex('0xFF')}")
    print(f"to_binary('0b1010') = {to_binary('0b1010')}")
    print(f"to_octal('0o777') = {to_octal('0o777')}")

if __name__ == '__main__':
    test_convert() 