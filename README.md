Nodoc
============
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Metrics](https://img.shields.io/badge/build-develop-yellow)

# Introduction

&emsp;&emsp;This tool can transform many kinds of documents to node, then we can operate those documents more easily. Node operation is also a common way to classify the data in some types of documents, when we united the structure of them, we'll get a more flexible way to manipulate the documents.

# Installation
This project is developed using Python 3.12.<br>
Use clone command.

`git clone https://github.com/HangBack/nodoc.git`

Setting up a Conda environment with Python 3.12 using the command.


`conda create -n {env_name} python==3.12`

Activate.

`conda activate {env_name}`<br>

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
&emsp;&emsp;However, in Nodoc, we don't individually place nodes into memory; instead, we use a fundamental container, the "basic tree," to store all nodes.<br>
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

# Contributors
- **HangBack**: Build the entire project.