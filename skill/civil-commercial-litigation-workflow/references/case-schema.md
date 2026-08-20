# 案件主数据结构

## 必填区

- `case_identity`: 案件名称、案由、程序、阶段、法院、案号、立案日。
- `representation`: 委托人、诉讼地位、对方及其他参与人。
- `claims`: 每项诉请、金额、计算公式、截止日、法律及合同依据。
- `fact_timeline`: 事件ID、日期、日期精度、相对顺序、事实、来源、状态。
- `evidence_status`: 证据名称、待证事实、来源、真实性状态、缺口和补强动作。
- `procedure_status`: 送达、缴费、保全、答辩、举证、开庭、调解、裁判、上诉、执行。
- `open_issues`: 矛盾、未知事实、影响、处理规则和优先级。
- `workflow_outputs`: 已生成成果、版本、更新时间和适用阶段。

## 状态值

- `document_verified`: 已由原件或可靠电子文件核验。
- `lawyer_confirmed`: 律师确认但尚无文件入库。
- `party_reported`: 当事人陈述，待证据支持。
- `sequence_confirmed_date_unconfirmed`: 先后顺序确认，具体日期未知。
- `unknown`: 未知，不作推定。
- `conflict`: 与既有信息冲突，等待处理。

所有事实记录来源路径或可识别名称。旧值不得因新材料而无痕消失。

