# ISO 20022 表单生成器 Skill 包

这是给主流 agent 和 IDEA 共同使用的共享包，面向 ISO 20022 表单生成器项目。

## 作用

- 检查和修改 ISO 20022 表单生成器工作区。
- 从 schema JSON 或 PDF 重新生成表单输出。
- 验证 IE8 兼容 HTML、JS API、联动字段、循环组和嵌入浏览器流程。
- 给 Codex、其他 agent、IDEA 里的脚本流程提供同一套约定。

## 安装

把 skill 目录复制到对应环境可识别的位置：

`skill-package/iso20022-form-generator` -> `$CODEX_HOME/skills/iso20022-form-generator`

Codex 需要重启后加载新 skill；其他 agent 和 IDEA 则直接读取这个目录里的 README 和 scripts。

## 结构

- `iso20022-form-generator/SKILL.md` - Codex 真正读取的 skill 定义
- `iso20022-form-generator/agents/openai.yaml` - UI 元信息
- `iso20022-form-generator/scripts/` - 可选脚本资源。这里的 `.py` 可同时给 agent 和 IDEA 调用

## 现在怎么用

- 现在这个仓库里的 Python 工具，仍然直接放在工作区根目录 `scripts/`
- `SKILL.md` 只负责给 Codex 提示工作方式，不限制其他 agent 或 IDEA 的调用方式
- 所以现阶段可以继续这样调用：

```bash
python scripts/generate_form.py --schema output/<message_id>.json
python scripts/parse_pdf.py <input.pdf>
```

## 以后怎么用脚本

- 如果某个 `.py` 需要跟这个包一起分发、反复复用，就放到 `iso20022-form-generator/scripts/`
- 安装到 `$CODEX_HOME/skills/iso20022-form-generator` 后，Codex 就能按相对路径执行；
- 其他 agent 和 IDEA 也可以直接按这个目录调用同一份脚本：

```bash
python scripts/<file>.py ...
```

- 新增脚本时，再在 `SKILL.md` 里写清文件名、用途和入口即可，不需要把脚本内容抄进文档
