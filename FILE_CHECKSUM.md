# 文件哈希校验模块

这是一个无第三方依赖的 Python 模块，可以计算和验证文件的 MD5、SHA-1、SHA-256 或 SHA-512 哈希值。它会分块读取文件，也适合处理大文件。

计算 SHA-256：

```bash
python -m src.file_checksum readme.md
```

使用 MD5，并验证预期值：

```bash
python -m src.file_checksum readme.md --algorithm md5 --verify <预期哈希值>
```

运行测试：

```bash
python -m unittest discover -v
```
