package frame

import "strings"

/*
使用前缀树实现路由匹配
*/
type node struct {
	patten   string  // 匹配路由
	part     string  //匹配路由中的一部分
	children []*node // 子节点
	isWild   bool    //是否精确匹配 part中含有：或者*时为true
}

// matchChild
func (n *node) matchChild(part string) *node {
	for _, child := range n.children {
		if child.part == part || child.isWild {
			return child
		}
	}
	return nil
}

// matchChildren 匹配查找节点
func (n *node) matchChildren(part string) []*node {
	nodes := make([]*node, 0)
	for _, child := range n.children {
		if child.part == part || child.isWild {
			nodes = append(nodes, child)
		}
	}
	return nodes
}

// insert 递归插入节点 从顶层往下层 层层查找并插入
func (n *node) insert(patten string, parts []string, height int) {
	if len(parts) == height {
		n.patten = patten
		return
	}
	part := parts[height]
	child := n.matchChild(part)
	if child == nil {
		child = &node{part: part, isWild: part[0] == ':' || part[0] == '*'}
		n.children = append(n.children, child)
	}
	child.insert(patten, parts, height+1)
}

// search 递归查询节点
func (n *node) search(parts []string, height int) *node {
	if len(parts) == height || strings.HasPrefix(n.part, "*") {
		if n.patten == "" {
			return nil
		}
		return n
	}
	part := parts[height]
	children := n.matchChildren(part)
	for _, child := range children {
		result := child.search(parts, height+1)
		if result != nil {
			return result
		}
	}
	return nil
}
