#coding="utf-8"

list_number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # 


class Node:
    def __init__(self, left: "Node", right: "Node", l:int, r:int, sum_node: int) -> None:
        self.left = left
        self.right = right
        self.l = l
        self.r = r
        self.sum_node = sum_node

def build(l, r):
    if  l + 1 == r:
        # лист, правая граница не входит в интервал
        return Node(None, None, l, r, sum_node=list_number[l])  
    else:
        m = int((r + l) / 2)  # (r - l) // 2
        node_l = build(l, m) 
        node_r = build(m, r)
        return Node(node_l, node_r, l, r, node_l.sum_node + node_r.sum_node)


def change(cur_node, ind, val):
    chaild_node = None
    old = cur_node.sum_node
    if cur_node.left == None:
        # дошли до листа
        cur_node.sum_node = val
        return old
    if ind < cur_node.left.r:
        chaild_node = cur_node.left
        old_chaild = change(chaild_node, ind, val)
        cur_node.sum_node = cur_node.sum_node - old_chaild + chaild_node.sum_node
        return old
    if ind > cur_node.right.l:
        chaild_node = cur_node.right
        old_chaild = change(chaild_node, ind, val)
        cur_node.sum_node = cur_node.sum_node - old_chaild + chaild_node.sum_node
        return old
    elif ind == cur_node.right.l:
        chaild_node = cur_node.right
        old_chaild = change(chaild_node, ind, val)
        cur_node.sum_node = cur_node.sum_node - old_chaild + chaild_node.sum_node
        return old

def get(node, l, r):
    sum = 0
    
    if node.l + 1 == node.r:
        # leaf
        return node.sum_node

    if r < node.l or l > node.r:
        return 0
    
    if node.l >= l and node.r <= r:
        sum += node.sum_node
        return sum
    
    if l < node.left.r:
        sum += get(node.left, l, r)
    
    if r > node.right.l:
        sum += get(node.right, l, r) 

    return sum         




root = build(0, len(list_number))    
print(root.sum_node)  
# change(root, 2, 13)
print(root.sum_node)
print(get(root, 3, 8))
print()