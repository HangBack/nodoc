[**English**](README.md) | 中文

Nodoc: 层层分级，轻松高效地操控文档数据
============
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Metrics](https://img.shields.io/badge/build-develop-yellow)

# 介绍

&emsp;&emsp;本工具可将许多文档数据节点化，将文档以这种形式分层后，我们将更容易便捷的操作文档。节点操作也是一些文档类型中常用的数据分类手段，当我们将所有文档统一化为一种结构，这会使得文档操作变得更加灵活。

# 安装
本项目使用python 3.11版本，将项目clone到本地。

`git clone https://github.com/HangBack/nodoc.git`

创建python 3.11的conda环境。


`conda create -n {env_name} python==3.11`

激活环境，并使用python 3.11解释器。

`conda activate {env_name}`<br>

安装requirements.txt。

`pip install -r requirements.txt`<br>

# 快速上手
## 基本节点
&emsp;&emsp;在Nodoc中，我们倾向于链式调用的方式操作节点属性，下面这个示例中描述了我们如何创建一个基本节点。<br>
**示例程序**

``` py
# example.py
from nodoc import Node

myNode = Node(content='我是一个节点') # 传入**data，关键字参数
myRootNode = Node(content='根节点')
myNode.parent = myRootNode # 将myNode节点的父节点设置为myRootNode节点
print(myNode.parent.children[0].data['content'])
```
<details>
    <summary style="cursor: pointer;">输出逻辑</summary>
&emsp;&emsp;myNode.parent 访问其父节点，即myRootNode<br>
&emsp;&emsp;myNode.parent.children[0] 访问myRootNode下的第一个子节点，由于myNode是唯一一个选择它作为父节点的节点，固然第一个子节点是myNode<br>
&emsp;&emsp;myNode.parent.chidlren[0].data 访问该节点的数据<br>
</details>
<br>

**输出**

``` console
> python example.py
我是一个节点
```
## 基本树
&emsp;&emsp;然而，在Nodoc中，我们并不单独的去将节点放到内存当中，而使用一种基本容器“基本树”去存储所有的节点。<br>
**示例程序**

``` py
# example2.py
from example import myRootNode
from nodoc import Tree

myTree = Tree(root = myRootNode, name = '我的树')
print(myTree.name, myTree.root.data['content'])
print(*[i.data for i in myTree.BFT()], sep='\n') # 通过树的层次遍历方法输出节点数据
```
**输出**

``` console
> python example2.py
我是一个节点
我的树 根节点
{'content': '根节点'}
{'content': '我是一个节点'}
```

## 文档节点与文档树
&emsp;&emsp;上述示例中，我们并没有真正体验到Nodoc的特殊之处，为了使文档操作更加方便与准确，Nodoc实现了文档节点和文档树，我们文档的各种属性也将被存储在文档树的属性中。下面我们将通过更合理的数据结构以规范的存储我们的文档。<br>
**示例程序**

``` py
# example3.py
from nodoc import docNode, docTree
    
titleNode = docNode(kind = 'title', content = '标题A')
contextNode = docNode(content = '我是一段正文，一段正文……' * 256)
contextNode.parent = titleNode
myDocTree = docTree(titleNode, '我的文档树')
myDocTree.toMarkdown()
print(myDocTree)
```

**输出**

``` console
> python example3.py
我的文档树
- 创建时间：%Y-%m-%d %H:%M:%S
- 修改时间：%Y-%m-%d %H:%M:%S
- 访问时间：%Y-%m-%d %H:%M:%S
- 文档大小：6.57KB
- 文档内容：# 标题A...(3325字)...段正文……
```
<details>
<summary style="cursor: pointer;"><strong>稍微复杂的例子</strong></summary>

**示例程序**

``` py
# example4.py
from nodoc import docNode, docTree

rootNode = docNode(kind='text', content='')
titleNodeA = docNode(kind = 'title', content = '标题A')
titleNodeB = docNode(kind = 'title', content = '标题B')
titleNodeAa = docNode(kind = 'title', content = '标题Aa')
contextNodeA = docNode(content = '我是一段正文，一段正文……' * 5)
contextNodeB = docNode(content = '我是一段正文，一段正文……' * 5)
titleNodeAa.parent = titleNodeA
contextNodeA.parent = titleNodeA
contextNodeB.parent = titleNodeB
titleNodeA.parent = rootNode
titleNodeB.parent = rootNode
myDocTree = docTree(rootNode, '我的文档树')
myDocTree.toMarkdown()
print(myDocTree.document, myDocTree)
```

**输出**

``` console
> python example4.py
# 标题A
## 标题Aa
我是一段正文，一段正文……我是一段正文，一段正文……我是一段正文，一段正文……我是一段正文，一段正文……我是一段正文，一段正文……
# 标题B
我是一段正文，一段正文……我是一段正文，一段正文……我是一段正文，一段正文……我是一段正文，一段正文……我是一段正文，一段正文……

我的文档树
- 创建时间：%Y-%m-%d %H:%M:%S
- 修改时间：%Y-%m-%d %H:%M:%S
- 访问时间：%Y-%m-%d %H:%M:%S
- 文档大小：364.00B
- 文档内容：# 标题...(143字)...段正文……
```

</details>

## 向量数据库
&emsp;&emsp;既然我们已经可以将文档节点化了，那我们有没有什么好的方式去将它们存储在内存空间中呢。Nodoc提供了向量数据库，方便了我们对节点内容的模糊查询。<br>
**示例程序**

``` py
# example5.py
from nodoc import docNode, docTree

rootNode = docNode(kind='text', content='')
titleNodeA = docNode(kind = 'title', content = '小狗标题')
titleNodeB = docNode(kind = 'title', content = '小猫标题')
contextNodeA = docNode(content = '我是一只小狗')
contextNodeB = docNode(content = '我是一只小猫')
contextNodeA.parent = titleNodeA
contextNodeB.parent = titleNodeB
titleNodeA.parent = rootNode
titleNodeB.parent = rootNode
myDocTree = docTree(rootNode, '我的文档树')

from nodoc import vectorDB

db = vectorDB([myDocTree]) # 创建数据库



x = db.query('小猫').parent.data['content'] # 查询含有“小猫”的节点的标题

newNode = docNode(content = '我是一只狐狸')
newTitle = docNode(kind = 'title', content = '狐狸标题')
newNode.parent = newTitle

db.insert(1, newNode) # 增加一个节点，该节点的标题是“狐狸标题”


y = db.query('狐狸').parent.data['content'] # 查询含有“狐狸”的节点的标题
print(x, y)
```

**输出**

``` console
> python example5.py
小猫标题 狐狸标题
```

&emsp;&emsp;我们通过vectorDB实例export方法将数据库导出，导入时通过vectorDB的静态方法load从磁盘中导入扩展名为nodocdb的文件<br>
例如刚刚的示例中

**示例程序**

```py
# example6.py
from example5 import db
db.export('mydatabase', './')

```

**输出**

``` console
> python example6.py
> 
```

接下来我们导入这个数据库

**示例程序**

```py
# example7.py
from nodoc import vectorDB
db = vectorDB.load('./mydatabase.nodocdb')
x = db.query('狐狸').parent.data['content']
print(x)

```

**输出**

``` console
> python example7.py
狐狸标题
```

# 贡献
- **HangBack**: 构建整个项目