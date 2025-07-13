from elasticsearch import Elasticsearch
from datetime import datetime
import uuid  # 用于生成唯一 uuid

# ✅ 初始化 ES 客户端
es = Elasticsearch("http://localhost:9200")

content_text = """
物模型，物模型规范，物模型样式，物模型格式
result_json = {
        "components": [{
        "componentKey": "必须",
        "componentName": "必须",
        "domainType": 0,
        "events": [{
            "description": "",
            "domainType": 0,
            "eventKey": "必须",
            "eventName": "必须",
            "eventType": "事件类型：alarm（告警），information（信息），error（故障）",
            "flag": 1,
            "id": "661796a74e66db0dd48614b0",
            "influxFlag": 2,
            "key": "",
            "labelCode": "",
            "labelName": "",
            "name": "事件名称",
            "necessary": "必须：true /false",
            "outputData": [{
                "dataType": {
                    "specifications": {
                        "length": "长度（text）",
                        "minimum ": "参数最小值（Integer、float、double类型特有）",
                        "maximum ": "参数最大值（Integer、float、double类型特有）",
                        "unit": "参数单位",
                        "unitName": "单位名称",
                        "size": "数组大小，默认最大128（数组特有）。",
                        "step": "步长，字符串类型。"
                    },
                    "type": "必须：参数类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）"

                },
                "key": "必须：参数标识符",
                "name": "必须：参数名称",
                "necessary": "必须: True / false",
                "paramKey": "参数标识符",
                "paramName": "参数名称"
            }],
            "type": "必须：事件类型：alarm（告警），information（信息），error（故障）",
            "version": 1.0
        }],
        "flag": 1,
        "id": "6611f9b3064e801a5839de52",
        "imgPath": "",
        "properties": [{
            "accessMethod": "必须：属性访问方式：只读（r）或读写（rw）。",
            "dataType": {
                "specifications": {
                    "length": "必须：长度（text）",
                    "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                    "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                    "unit": "必须：属性单位",
                    "unitName": "必须：单位名称",
                    "size": "必须：数组大小，默认最大128（数组特有）。",
                    "step": "必须：步长，字符串类型。",
                    " item": {
                        "type": "必须：数组元素的类型"
                    }
                },
                "type": "必须：属性类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）、struct（结构体类型，可包含前面7种类型）、Array（数组类型，支持Integer/double/float/text/struct）"
            },
            "description": "属性描述",
            "domainType": 0,
            "flag": 0,
            "influxFlag": 2,
            "key": "属性唯一标识符",
            "labelCode": "",
            "labelName": "",
            "name": "属性名称",
            "necessary": "必须： true/false",
            "propertyKey": "必须：属性唯一标识符",
            "propertyName": "必须：属性名称"
        }],
        "services": [{
            "callMethod": "必须：asynchronization、synchronization",
            "description": "",
            "domainType": 0,
            "flag": 1,
            "id": "661796334e66db0dd48614af",
            "influxFlag": 2,
            "inputData": [{
                "dataType": {
                    "specifications": {
                        "length": "必须：长度（text）",
                        "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                        "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                        "unit": "必须：参数单位",
                        "unitName": "必须：单位名称",
                        "size": "必须：数组大小，默认最大128（数组特有）。",
                        "step": "必须：步长，字符串类型。"
                    },
                    "type": "必须：参数类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）"
                },
                "key": "必须：参数标识符",
                "name": "必须：参数名称",
                "necessary": "必须：true/false",
                "paramKey": "参数标识符",
                "paramName": "参数名称"
            }],
            "key": "",
            "labelCode": "",
            "labelName": "",
            "name": "",
            "necessary": "必须： true/false",
            "outputData": [{
                "dataType": {
                    "specifications": {
                        "length": "必须：长度（text）",
                        "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                        "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                        "unit": "必须：参数单位",
                        "unitName": "必须：单位名称",
                        "size": "必须：数组大小，默认最大128（数组特有）。",
                        "step": "必须：步长，字符串类型。"
                    },
                    "type": "必须：参数类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）"
                },
                "key": "必须：Return_parameter",
                "name": "必须：返回参数",
                "necessary": "必须： true/false",
                "paramKey": "Return_parameter",
                "paramName": "返回参数"
            }],
            "serviceKey": "必须：服务key",
            "serviceName": "必须：服务名称",
            "version": 1.0
        }],
        "version": 1.0
    }],
        "events": [
            {
                "description": "",
                "domainType": 0,
                "eventKey": "必须",
                "eventName": "必须",
                "eventType": "事件类型：alarm（告警），information（信息），error（故障）",
                "flag": 1,
                "id": "661796a74e66db0dd48614b0",
                "influxFlag": 2,
                "key": "事件key",
                "labelCode": "",
                "labelName": "",
                "name": "事件名称",
                "necessary": "必须： true/false",
                "outputData": [{
                    "dataType": {
                        "specifications": {
                            "length": "必须：长度（text）",
                            "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                            "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                            "unit": "必须：参数单位",
                            "unitName": "必须：单位名称",
                            "size": "必须：数组大小，默认最大128（数组特有）。",
                            "step": "必须：步长，字符串类型。"
                        },
                        "type": "参数类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）"
                    },
                    "key": "必须：参数标识符",
                    "name": "必须：参数名称",
                    "necessary": "必须：True/false",
                    "paramKey": "参数标识符",
                    "paramName": "参数名称"
                }],
                "type": "必须：事件类型：alarm（告警），information（信息），error（故障）",
                "version": 1.0
            }
        ],
        "firmInfo": "厂商信息",
        "imgPath": "",
        "key": "key",
        "name": "name",
        "profile": {
            "categoryKey": "categoryKey",
            "productKey": "productKey"
        },
        "properties": [{
            "accessMethod": "必须：属性访问方式：只读（r）或读写（rw）。",
            "dataType": {
                "specifications": {
                    "length": "必须：长度（text）",
                    "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                    "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                    "unit": "必须：参数单位",
                    "unitName": "必须：单位名称",
                    "size": "必须：数组大小，默认最大128（数组特有）。",
                    "step": "必须：步长，字符串类型。"
                },
                "type": "必须：属性类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）、struct（结构体类型，可包含前面7种类型）、Array（数组类型，支持Integer/double/float/text/struct）"
            },
            "description": "",
            "domainType": 0,
            "flag": 1,
            "id": "6673d8d7bf55584995470b4e",
            "influxFlag": 2,
            "key": "属性唯一标识符",
            "name": "属性名称",
            "necessary": "必须：true/false",
            "propertyKey": "必须：属性唯一标识符",
            "propertyName": "必须：属性名称",
            "version": 2.0
        }],
        "providerType": "0",
        "services": [{
            "callMethod": "必须：asynchronization/synchronization",
            "description": "",
            "domainType": 0,
            "flag": 1,
            "id": "661796334e66db0dd48614af",
            "influxFlag": 2,
            "inputData": [{
                "dataType": {
                    "specifications": {
                        "length": "必须：长度（text）",
                        "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                        "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                        "unit": "必须：参数单位",
                        "unitName": "必须：单位名称",
                        "size": "必须：数组大小，默认最大128（数组特有）。",
                        "step": "必须：步长，字符串类型。"
                    },
                    "type": "必须：参数类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）"
                },
                "key": "必须",
                "name": "必须",
                "necessary": "必须：true/false",
                "paramKey": "参数标识符",
                "paramName": "参数名称"
            }],
            "key": "服务key",
            "labelCode": "",
            "labelName": "",
            "name": "服务名称",
            "necessary": "必须：true/false",
            "outputData": [{
                "dataType": {
                    "specifications": {
                        "length": "必须：长度（text）",
                        "minimum ": "必须：参数最小值（Integer、float、double类型特有）",
                        "maximum ": "必须：参数最大值（Integer、float、double类型特有）",
                        "unit": "必须：参数单位",
                        "unitName": "必须：单位名称",
                        "size": "必须：数组大小，默认最大128（数组特有）。",
                        "step": "必须：步长，字符串类型。"
                    },
                    "type": "必须：参数类型: Integer（原生）、float（原生）、double（原生）、text（原生）、date（String类型UTC毫秒）、bool（0或1的Integer类型）、enum（Integer类型）"
                },
                "key": "Return_parameter",
                "name": "必须：返回参数",
                "necessary": "必须：true/false",
                "paramKey": "Return_parameter",
                "paramName": "返回参数"
            }],
            "serviceKey": "服务key",
            "serviceName": "服务名称",
            "version": 1.0
        }],
        "standardList": "200001",
        "thingModelKey": "必须：thingModelKey",
        "thingModelName": "必须：thingModelName",
        "updateDesc": "",
        "version": 1.0
}


"""


# ✅ 构造文档数据（自动生成 uuid）
doc = {
    "category": ["物模型"],
    "content": content_text.strip(),
    "creat_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "file_id": "file001",
    "uuid": str(uuid.uuid4())  # 自动生成唯一 UUID 字符串
}

# ✅ 索引名称
index_name = "knowledge_base"

# ✅ 使用 uuid 作为 _id 插入文档
res = es.index(index=index_name, body=doc)

# ✅ 打印插入结果
print(res)