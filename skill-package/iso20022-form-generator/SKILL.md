---
name: iso20022-form-generator
description: 检查、修改、重新生成并验证 ISO 20022 表单生成器项目，包括解析器、渲染器、API、生成的 HTML 和嵌入浏览器检查。用于处理本工作区的 ISO 20022 表单生成器源码、output/form 产物、IE8 兼容性、循环组、字段联动、校验或浏览器回归问题。
---

# ISO 20022 表单生成器

## 总览

用于这个 ISO 20022 表单生成器工作区。把 `scripts/` 视为源码，把 `output/form/` 视为生成产物，改动要尽量收敛。这里的约定主要给 Codex 使用，也便于其他 agent 和 IDEA 读取同一套脚本资源。

## 流程

1. 在改行为前先读仓库根目录的 `SKILL.md` 和 `CLAUDE.md`。
2. 先改 `scripts/` 里的源码。
3. 当已有 schema 输入时，用 `python scripts/generate_form.py --schema output/<message_id>.json` 重新生成输出。
4. 只有在需要从规范 PDF 重新构建 schema 时，才走 PDF 解析流程。

## 验证

- 运行 `python -m py_compile scripts/form_api.py scripts/form_app.py scripts/form_page.py scripts/generate_form.py`。
- 运行 `node --check output/form/js/app.js` 以及对应的消息 API 文件。
- 在浏览器中打开 `output/form/<safe_name>.html` 和 `output/form/embed_api_test.html`。
- 检查重复 id、控制台错误、横向溢出和 API 隔离是否正常。

## 关键路径

- 源码：`scripts/form_api.py`、`scripts/form_app.py`、`scripts/form_page.py`、`scripts/field_renderer.py`、`scripts/generate_form.py`
- 输出：`output/form/`
- Schema：`output/*.json`

## 脚本资源

- 当前 skill 包还没有额外内置 Python 脚本。
- 这个仓库里的现有 Python 工具，仍然直接使用工作区根目录下的 `scripts/`，例如：
  - `python scripts/generate_form.py --schema output/<message_id>.json`
  - `python scripts/parse_pdf.py <input.pdf>`
- 如果后续要把通用工具打包进这个共享包，把可复用脚本放到 `skill-package/iso20022-form-generator/scripts/`。
- 这样安装到 `$CODEX_HOME/skills/iso20022-form-generator` 后，Codex、其他 agent 和 IDEA 脚本流程都可以按相对路径执行这些脚本：
  - `python scripts/<file>.py ...`
- 新增脚本时，只需要在这里按文件名写清用途和入口，不必把脚本正文抄进 `SKILL.md`。

## 备注

- 保持 ES5 和 IE8 兼容。
- 优先修 API 层，不要只写一次性的 DOM 兜底。
- 源码改完后要重新生成输出。
