# 1. Find S
#       ↓
# 2. DFS/BFS from S
#       ↓
# 3. At each state:
#       position
#       energy remaining
#       litter collected
#       ↓
# 4. Try 4 directions
#       ↓
# 5. Reject invalid moves / X / insufficient energy
#       ↓
# 6. Moving costs 1 energy
#       ↓
# 7. L → mark collected
# 8. R → reset energy
#       ↓
# 9. All L collected → answer
#       ↓
# 10. Add visited/DP to avoid repeating states
from collections import deque

class Solution:
    def minMoves(self, classroom: List[str], energy: int) -> int:
        rows = len(classroom)
        cols = len(classroom[0])

        # Find start and give every L an ID
        start = None
        litter_id = {}
        litter_count = 0

        for i in range(rows):
            for j in range(cols):
                if classroom[i][j] == 'S':
                    start = (i, j)
                elif classroom[i][j] == 'L':
                    litter_id[(i, j)] = litter_count
                    litter_count += 1

        
        target = (1 << litter_count) - 1

        
        q = deque([(start[0], start[1], energy, 0, 0)])

       
        visited = {(start[0], start[1], energy, 0)}

        directions = [
            (-1, 0), 
            (1, 0),   
            (0, -1),  
            (0, 1)   
        ]

        while q:
            i, j, curr_energy, mask, moves = q.popleft()

            
            if mask == target:
                return moves

           
            if curr_energy == 0:
                continue

            for di, dj in directions:
                ni = i + di
                nj = j + dj

                
                if ni < 0 or ni >= rows or nj < 0 or nj >= cols:
                    continue

                
                if classroom[ni][nj] == 'X':
                    continue

                
                new_energy = curr_energy - 1
                new_mask = mask

                
                if classroom[ni][nj] == 'L':
                    litter = litter_id[(ni, nj)]
                    new_mask |= (1 << litter)

               
                if classroom[ni][nj] == 'R':
                    new_energy = energy

                state = (ni, nj, new_energy, new_mask)

                if state in visited:
                    continue

                visited.add(state)
                q.append((ni, nj, new_energy, new_mask, moves + 1))

        return -1
