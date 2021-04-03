from binarytree import Node, tree

def minimax(position, depth, alpha, beta, maximizingPlayer):
  if depth == 0:
    return position.value

  if maximizingPlayer == 'true':
    maxEval = float('-inf')
    val = minimax(position.left, depth - 1, alpha, beta, 'false')
    maxEval = max(maxEval, val)
    alpha = max(alpha, val)
    if beta > alpha:
      val = minimax(position.right, depth - 1, alpha, beta ,'false')
      maxEval = max(maxEval, val)
      alpha = max(alpha, val)
    position.value = maxEval
    return maxEval

  else:
    minEval = float('inf')
    val = minimax(position.left, depth - 1, alpha, beta, 'true')
    minEval = min(minEval, val)
    beta = min(beta, val)
    if beta > alpha:
      val = minimax(position.right, depth - 1, alpha, beta, 'true')
      minEval = min(minEval, val)
      beta = min(beta, val)
    position.value = minEval  
    return minEval

root = Node(0)
root.left =Node(0)
root.right = Node(0)
root.left.left = Node(0)
root.left.right = Node(0)
root.right.left = Node(0)
root.right.right = Node(0)
root.left.left.left = Node(4)
root.left.left.right = Node(9)
root.left.right.left = Node(2)
root.left.right.right = Node(1)
root.right.left.left = Node(5)
root.right.left.right = Node(7)
root.right.right.left = Node(3)
root.right.right.right = Node(6)

print("Original tree:")
print(root)
ans = minimax(root, root.height, float('-inf'), float('inf'), 'true')
print("\nalpha-beta tree:")
print (root)
print("The alpha-beta pruning value is: ", ans)
