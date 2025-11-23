import heapq

class AStarPathFinding:
    def __init__(self, maze, start_pos, target_pos):
        self.maze = maze
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.open_set = []
        self.closed_set = set()
        self.came_from = {}
        # self.g_score = {start_pos: 0}
        # self.f_score = {start_pos: self.heuristic(start_pos, target_pos)}
        # heapq.heappush(self.open_set, (self.f_score[start_pos], start_pos))
        
    def heuristic(self, a, b):
        # Using Manhattan distance as heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self, pos):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for direction in directions:
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if self.is_valid_position(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    def is_valid_position(self, pos):
        row, col = pos
        return (0 <= row < len(self.maze) and 0 <= col < len(self.maze[0])) and self.maze[row][col] == 1
    
    def reconstruct_path(self, current):
        total_path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            total_path.append(current)
        return total_path[::-1]  # Return reversed path
    
    def find_path(self):
        heapq.heappush(self.open_set, (0, self.start_pos))
        
        g_score = {self.start_pos: 0}
        f_score = {self.start_pos: self.heuristic(self.start_pos, self.target_pos)}
        
        while self.open_set:
            _, current = heapq.heappop(self.open_set)
            
            if current == self.target_pos:
                return self.reconstruct_path(current)
            
            self.closed_set.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor in self.closed_set:
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.target_pos)
                    heapq.heappush(self.open_set, (f_score[neighbor], neighbor))
                    
        return None

def render_maze(maze, path=None, start=None, target=None):
    """Render the maze to stdout.
    Walls (0) shown as '#', open cells (1) as '.'.
    Path cells overridden with '█'. Start shown as 'S', target as 'T'.
    """
    path_set = set(path) if path else set()
    for r, row in enumerate(maze):
        line_chars = []
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start:
                line_chars.append('S ')
            elif pos == target:
                line_chars.append('T ')
            elif pos in path_set:
                line_chars.append('█ ')
            else:
                if cell == 0:
                    line_chars.append('# ')
                else:
                    line_chars.append('. ')
        print(''.join(line_chars))
    print()  # blank line for spacing
    
if __name__ == "__main__":
    maze = [
        [1, 1, 1, 0, 1],
        [0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
    ]
    complex_maze = [
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    start_pos = (0, 0)
    target_pos = (4, 4)
    
    pathfinder = AStarPathFinding(complex_maze, start_pos, target_pos)
    print("Initial maze:")
    render_maze(complex_maze, start=start_pos, target=target_pos)
    path = pathfinder.find_path()
    
    if path:
        print("Path found:", path)
        print("Maze with path:")
        render_maze(complex_maze, path=path, start=start_pos, target=target_pos)
    else:
        print("No path found.")