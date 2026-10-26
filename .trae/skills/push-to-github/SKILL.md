---
name: "push-to-github"
description: "将本项目提交并推送到 GitHub 远程仓库 https://github.com/zwd-wen/zhengwendi。当用户要求提交代码、推送、push 到 GitHub、同步到远程仓库时调用此技能。"
---

# Push to GitHub

将本地项目提交并推送到 GitHub 远程仓库。

## 远程仓库信息

- **仓库地址**：`https://github.com/zwd-wen/zhengwendi`
- **认证方式**：SSH 公钥（已配置）
- **默认分支**：`master`

## 执行步骤

### 1. 检查远程仓库配置

```powershell
git remote -v
```

- 如果 `origin` 不存在或地址不对，设置/修正远程地址：
  ```powershell
  git remote add origin https://github.com/zwd-wen/zhengwendi
  # 或
  git remote set-url origin https://github.com/zwd-wen/zhengwendi
  ```

### 2. 查看当前变更状态

```powershell
git status --short
```

向用户展示当前的修改/新增文件清单，**确认提交范围**（是全部提交还是仅指定文件）。

### 3. 暂存并提交

- **全部提交**：`git add -A`
- **指定文件**：`git add <文件路径>`

提交信息使用中文，格式清晰描述本次改动内容。例如：
```
新增 15-1.html：数7游戏（100个盒子，7的倍数与尾数为7显示空盒子）
```

提交命令：
```powershell
git commit -m "<提交信息>"
```

### 4. 推送到远程仓库

```powershell
git push origin master
```

如果是首次推送且远程分支不存在，使用：
```powershell
git push -u origin master
```

### 5. 验证推送结果

```powershell
git log --oneline -3
git status
```

确认工作区干净、提交已同步到远程。

## 注意事项

1. **提交范围确认**：执行 `git add` 前必须先通过 `git status` 展示变更清单，并向用户确认提交范围（全部 / 指定文件），避免误提交无关文件。
2. **PowerShell 兼容**：本项目运行在 Windows PowerShell 环境，不要使用 `&&`、`||`、`heredoc` 等 bash 语法，使用 `;` 分隔命令。
3. **换行符警告**：Windows 下 Git 可能提示 `LF will be replaced by CRLF`，这是正常警告，不影响提交。
4. **推送失败排查**：
   - 若提示认证失败，确认 SSH 公钥已添加到 GitHub 账户
   - 若提示非快进（non-fast-forward），先 `git pull origin master --rebase` 拉取并变基，再推送
   - 若提示分支不存在，使用 `-u` 参数建立上游追踪关系
5. **不主动修改历史**：除非用户明确要求，不要使用 `git push --force` 强制推送。
