English | [**中文**](README.zh.md)

Nodoc: Layer-by-layer manipulation of document data with ease and efficiency.
============
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Metrics](https://img.shields.io/badge/build-develop-yellow)

# Introduction

&emsp;&emsp;Nodoc is a powerful document processing tool that implements the document layer by nodeding various document data tiered storage and efficient operations. This hierarchical indexed storage method not only simplifies document management, but also enables users to: Easier data mining and cross-document operations.

# Installation
This project is developed using Python 3.11.<br>
Use clone command.

`git clone https://github.com/HangBack/nodoc.git`

Setting up a Conda environment with Python 3.11 using the command.


`conda create -n {env_name} python==3.11`

Activate.

`conda activate {env_name}`<br>

Install "requirements.txt".

`pip install -r requirements.txt`<br>

# Quick Start
## Base node
&emsp;&emsp;In Nodoc, we prefer operating on node attributes using a chained method invocation. The following example illustrates how we create a basic node.
**Example**

``` py
# example.py
from nodoc import Node

myNode = Node(content="I'm a node.") # Passing **data, keyword arguments.
myRootNode = Node(content='Root node')
myNode.parent = myRootNode # Set the parent node of the myNode to the myRootNode.
print(myNode.parent.children[0].data['content'])
```
<details>
    <summary style="cursor: pointer;">Output logic.</summary>
&emsp;&emsp;myNode.parent  # Access its parent node, i.e., myRootNode.<br>
&emsp;&emsp;myNode.parent.children[0]  # Access the first child node under myRootNode, as myNode is the only node choosing it as a parent, the first child is myNode.<br>
&emsp;&emsp;myNode.parent.children[0].data  # Access the data of that node.<br>
</details>
<br>

**Output**

``` console
> python example.py
I'm a node.
```
## Base Tree
&emsp;&emsp;However, in Nodoc, we don't individually place nodes into memory; instead, we use a fundamental container, the "base tree" to store all nodes.<br>
**Example**

``` py
# example2.py
from example import myRootNode
from nodoc import Tree

myTree = Tree(root = myRootNode, name = 'My tree')
print(myTree.name, myTree.root.data['content'])
print(*[i.data for i in myTree.BFT()], sep='\n') # Output node data through tree-level traversal method.
```
**Output**

``` console
> python example2.py
I'm a node.
My tree Root node
{'content': 'Root node'}
{'content': "I'm a node."}
```

## Document Node and Document Tree
&emsp;&emsp;In the above example, we haven't truly experienced the uniqueness of Nodoc. To make document operations more convenient and accurate, Nodoc implements document nodes and a document tree. Various properties of our document will be stored in the attributes of the document tree. Below, we will use a more reasonable data structure to systematically store our document.<br>
**Example**

``` py
# example3.py
from nodoc import docNode, docTree
    
titleNode = docNode(kind = 'title', content = 'Caption A')
contextNode = docNode(content = 'I am a body of text, a body of text...' * 256)
contextNode.parent = titleNode
myDocTree = docTree(titleNode, 'My document tree')
myDocTree.toMarkdown()
print(myDocTree)
```

**Output**

``` console
> python example3.py
My document tree
- 创建时间：%Y-%m-%d %H:%M:%S
- 修改时间：%Y-%m-%d %H:%M:%S
- 访问时间：%Y-%m-%d %H:%M:%S
- 文档大小：9.55KB
- 文档内容：# Cap...(9731字)...xt...
```

<details>
<summary style="cursor: pointer;"><strong>Output in English</strong></summary>

``` console
> python example3.py
My document tree:
- Creation Time: %Y-%m-%d %H:%M:%S
- Modification Time: %Y-%m-%d %H:%M:%S
- Access Time: %Y-%m-%d %H:%M:%S
- Document Size: 9.55KB
- Document Content: # Cap...(9731 words)...xt...
```

</details>
<br>
<details>
<summary style="cursor: pointer;"><strong>A slightly more complex example.</strong></summary>

**Example**

``` py
# example4.py
from nodoc import docNode, docTree

rootNode = docNode(kind='text', content='')
titleNodeA = docNode(kind = 'title', content = 'Caption A')
titleNodeB = docNode(kind = 'title', content = 'Caption B')
titleNodeAa = docNode(kind = 'title', content = 'Caption Aa')
contextNodeA = docNode(content = 'I am a body of text, a body of text...')
contextNodeB = docNode(content = 'I am a body of text, a body of text...')
titleNodeAa.parent = titleNodeA
contextNodeA.parent = titleNodeA
contextNodeB.parent = titleNodeB
titleNodeA.parent = rootNode
titleNodeB.parent = rootNode
myDocTree = docTree(rootNode, 'My document tree')
myDocTree.toMarkdown()
print(myDocTree.document, myDocTree)
```

**Output**

``` console
> python example4.py
# Caption A
## Caption Aa
I am a body of text, a body of text...
# Caption B
I am a body of text, a body of text...

我的文档树
- 创建时间：%Y-%m-%d %H:%M:%S
- 修改时间：%Y-%m-%d %H:%M:%S
- 访问时间：%Y-%m-%d %H:%M:%S
- 文档大小：158.00B
- 文档内容：# Ca...(107字)...xt...
```

<details>
<summary style="cursor: pointer;"><strong>Output in English</strong></summary>

``` console
> python example4.py
# Caption A
## Caption Aa
I am a body of text, a body of text...
# Caption B
I am a body of text, a body of text...

My document tree
- Creation Time: %Y-%m-%d %H:%M:%S
- Modification Time: %Y-%m-%d %H:%M:%S
- Access Time: %Y-%m-%d %H:%M:%S
- Document Size：158.00B
- Document Content：# Ca...(107字)...xt...
```

</details>

</details>

## Vector Database
&emsp;&emsp;Now that we can node documents, is there a good way to store them in memory? Nodoc provides a vector database that facilitates our fuzzy queries of node content.<br>
**Example**

``` py
# example5.py
from nodoc import docNode, docTree

rootNode = docNode(kind='text', content='')
titleNodeA = docNode(kind = 'title', content = 'Puppy Title')
titleNodeB = docNode(kind = 'title', content = 'Ketty Title')
contextNodeA = docNode(content = "I'm a puppy.")
contextNodeB = docNode(content = "I'm a ketty.")
contextNodeA.parent = titleNodeA
contextNodeB.parent = titleNodeB
titleNodeA.parent = rootNode
titleNodeB.parent = rootNode
myDocTree = docTree(rootNode, 'My document tree')

from nodoc.database.vectordb import vectorDB

db = vectorDB([myDocTree]) # Set up the database



x = db.query('Ketty').parent.data['content'] # Query the node contains "Ketty" and out its title

newNode = docNode(content = "I'm a fox.")
newTitle = docNode(kind = 'title', content = 'Fox Title')
newNode.parent = newTitle

db.insert(1, newNode) # Add one node, the node title is "Fox Title"


y = db.query('Fox').parent.data['content'] # Query the node contains "Fox" and out its title
print(x, y)
```

**Output**

``` console
> python example5.py
Ketty Title Fox Title
```

&emsp;&emsp;We export the database through the vectorDB instance 'export' method, and import a file with the nodocdb extension from disk through vectorDB's static method 'load' when importing<br>
Like the just example.

**Example**

```py
# example6.py
from example5 import db
db.export('mydatabase', './')

```

**Output**

``` console
> python example6.py
> 
```

Then we load the database.

**Example**

```py
# example7.py
from nodoc import vectorDB
db = vectorDB.load('./mydatabase.nodocdb')
x = db.query('Fox').parent.data['content']
print(x)

```

**Output**

``` console
> python example7.py
Fox Title
```

# Contributors
- **HangBack**: Build the entire project.