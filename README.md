# 后端

此处存放后端代码。

后端采用Flask构建，使用Flask-SQLAlchemy读写Mysql数据库，使用Flask-SocketIO实现Websocket协议。

## 环境要求

后端采用MySQL作为数据库，建议使用 **MariaDB** （MySQL的开源版本）。

后端运行在Python 3.10上，建议使用 **Anaconda** 建立Python虚拟环境。

## 后端运行方式

由于Dependabot经常更新后端使用的库版本，在每次从远程仓库同步后端后，应使用`pip install -r requirements.txt`重新安装依赖库。

如果数据库结构发生更改（或第一次运行后端），应在运行后端前按以下步骤重新建立数据库：
* 在终端中用root用户登录MySQL，并将`create_db.sql`中的SQL语句逐行输入终端。
* 激活后端使用的虚拟环境，并运行`create_db.py`。

在以上步骤都完成或者不需要进行后，直接用VsCode的调试选项（在`项目根目录/.vscode/launch.json`中已配置好，想要正常使用，需要确保VsCode打开的是项目根目录而不是后端目录）调试或运行后端。