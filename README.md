# [Yz-id](https://github.com/ml444/yz-id)
--------------

## Introduction
An ID generator for distributed microservices.
一个分布式ID生成器框架，适用于微服务领域的全局ID生成。基于snowflake的设计理念，
设计出这个可自行根据需要重新分配了各部分的bit位的ID生成器框架。

在分布式系统中，整体的业务被拆分成多个自治的微服务，每个微服务之间需要通过网络进行通信和交互，
由于网络的不确定性，会给系统带来各种各样的不一致问题，为了避免和解决不一致问题，
最重要的模式是做系统之间的实时核对和事后核对，核对的基础就是领域对象及系统间的请求需要有唯一ID来标识。

在源码的`extras`中已经举例出三种ID组合方式方案。
- 【Snowflake】:

    | 版本 | 毫秒级时间 | 机器ID | 序列号 |
    | --- | --------- | ----- | ----- |
    | 63  | 62-22     | 21-12 | 11-0  |

- 【Sonyflake】:

    | 版本 | 10毫秒级时间 | 序列号 | 机器ID |
    | --- | ----------  | ----- | ----- |
    | 63  | 62-24       | 23-16 | 15-0  |
    
- 【Anonymous】:
    - 【最大峰值】：
    
        | 版本 | 类型 | 生成方式 | 秒级时间 | 序列号 | 机器ID |
        | --- | ---- | ------ | ------- | ------ |-------|
        | 63  | 62   | 60-61  | 59-30   | 29-10 | 0-9   |
        
    - 【最小粒度】：
    
        | 版本 | 类型 | 生成方式 | 毫秒级时间 | 序列号 | 机器ID |
        | --- | ---- | ------ | --------- | ------|-------|
        | 63   | 62  | 60-61  | 59-20     | 19-10 | 0-9   |
        
    生成方式：(嵌入式，restful，中心分发）
    `anonymous`适用于一些杂糅的架构场景，可以应对各种情景下的ID生成方式。

## Quick start

**安装模块**
```shell
$ pip install yzid
```
如果上面的三种方案适用你需要的场景，可以直接使用：
```python
# Anonymous:
from yzid import get_id_service
time_epoch = 1610351662
idsvc1 = get_id_service(time_epoch=time_epoch, machine_code=1)
id1 = idsvc1.generate_id()

# Snowflake
from yzid import get_snowflake_service
time_epoch = 1610351662 * 1000
idsvc2 = get_snowflake_service(time_epoch=time_epoch, machine_code=1)
id2 = idsvc2.generate_id()

# Sonyflake
from yzid import get_sonyflake_service
time_epoch = 1610351662*100
idsvc3 = get_sonyflake_service(time_epoch=time_epoch, machine_code=1)
id3 = idsvc3.generate_id()
```

如果没有合适的，可以自定义组合方案。
自定义组合ID组成示例：
```python
from yzid.core.service import IdService


def get_id_service(
        time_epoch: int,
        machine_code: int,
        generate_method: int = 2,
        mode_type: int = 1,
        version: int = 0,
):
    """

    :param time_epoch:      时间起点
    :param machine_code:    机器序号
    :param generate_method: (嵌入式，restful，中心分发）
    :param mode_type:       (最大峰值，最小粒度)
    :param version:
    :return:
    """
    _type = {
        "max_peak": [
            ("machine",     (10, machine_code)),  # (<name>: (<bit_count>, <default_value>))
            ("sequence",    20),                  # (<name>: (<bit_count>, 0))
            ("duration",    30),
            ("method",      (2, generate_method)),
            ("type",        (1, 1)),
            ("version",     (1, version)),
        ],
        "min_granularity": [
            ("machine",     (10, machine_code)),
            ("sequence",    10),
            ("duration",    40),
            ("method",      (2, generate_method)),
            ("type",        (1, 0)),
            ("version",     (1, version)),
        ]
    }
    structure = _type.get("max_peak") if mode_type == 1 else _type.get("min_granularity")

    return IdService(
        structure=structure,
        time_epoch=time_epoch,
        time_unit=1 if mode_type == 1 else 10**3,  # 秒级和毫秒级的选择
        time_name="duration",
        sequence_name="sequence"
    )
```
`structure`参数必须是有序的可迭代对象，在设计组合时，低位在前，高位在后；
命名字段的值可以是`Tuple[int, int]`或`int`，只有单个int时，即只指定该组成部分占用的位数，默认值为0。

`structure`里的所有组成部分的位数总和必须为64，否则报异常错误。

在ID的组成部分中，有两个部分是必不可少的————`时间`和`序列号`，所以无论在`structure`中的命名组合是什么，
都必须在实例化时指明它们的名称：
```python
time_name="duration",
sequence_name="sequence"
```
这样的`yzid`才知道需要对哪个部分进行时间操作和累加操作。

`time_unit`是时间单位，为了告诉`yzid`是使用秒级、百毫秒级、十毫秒级、毫秒级、还是微秒级的；
`time_unit`必须是底数为10的指数值：
- 秒级 = 10**0 或 1
- 百毫秒级 = 10**1 或 10
- 十毫秒级 = 10**2 或 100
- 毫秒级 = 10**3 或 1000
- 微秒级 = 10**6 或 1000000

`time_epoch`是起始时间戳，是一个重要的参数，而且需要警惕。一旦启用，不可变更。否则可能会造成ID重复。

## Documentation

[暂无](https://github.com/ml444/yz-id/README.md).

