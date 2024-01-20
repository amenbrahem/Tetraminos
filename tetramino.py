from getkey import getkey
import copy
import os
import sys




def import_card(file_path):
    try:
        with open(file_path, 'r') as file:
            dimensions = tuple(map(int, file.readline().strip().split(',')))
        with open(file_path, 'r') as file:
            tetraminos = [line.strip().split(';;') for line in file if line.strip()]
            
            for i in range(len(tetraminos)):
                if tetraminos[i]==(5,4):
                    continue
                tetraminos[i].append((0, 0))  
                

            return dimensions, tetraminos

    except FileNotFoundError:
        print(f"Le fichier '{file_path}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'importation du fichier : {e}")




def check_win(w, h,grid):
    
    for i in range(1,w-1):
        for j in range(1,h):
            if(grid[i+w][j+h] == " |" or grid[i+w][j+h] == "| " or grid[i+w][j+h] == "--"):
                continue
            elif grid[i+w][j+h] == "  "  :
                return False
    return True

def create_grid(w, h):
    grid = [["  "] * (3 * w + 3) for _ in range(3 * h + 3)]
    
    x = ((3 * w + 2) - w) // 2
    y = ((3 * h + 2) - h) // 2
    for i in range(x, x + w):
        grid[y - 1][i] = grid[(3 * h + 2) - (y)][i] = "--"
    
    for i in range(y, y + h):
        grid[i][x - 1] = " |"
        grid[i][(3 * w + 2) - x] = "| "

    return grid
def create_bar(grid):
    grid = [row[:] for row in grid]
    w=(len(grid[0])-2)//3
    h=(len(grid)-2)//3
    x = ((3 * w + 2) - w) // 2
    y = ((3 * h + 2) - h) // 2
    for i in range(x, x + w):
        grid[y - 1][i] = grid[(3 * h + 2) - (y)][i] = "--"
    
    for i in range(y, y + h):
        grid[i][x - 1] = " |"
        grid[i][(3 * w + 2) - x] = "| "
    return grid
def som(coords,bool):
    s=1
    if bool:
        for i in range(len(coords)-1):
            if coords[i][0]!=coords[i+1][0]:
                s=s+1
    else :
        for i in range(len(coords)-1):
            if coords[i][1]!=coords[i+1][1]:
                s=s+1
    return s+1
            


def rotate_tetramino(tetramino, clockwise=True):
    coords = tetramino[0]
    min_x = min(coord[0] for coord in coords)
    min_y = min(coord[1] for coord in coords)
    max_x = max(coord[0] for coord in coords)
    max_y = max(coord[1] for coord in coords)
    matrix = [[0 for _ in range(max_y - min_y + 1)] for _ in range(max_x - min_x + 1)]
    for x, y in coords:
        matrix[x - min_x][y - min_y] = 1
    if clockwise:
        matrix = list(zip(*matrix[::-1]))
    else:
        matrix = list(zip(*matrix))[::-1] 
    new_coords = [(x + min_x, y + min_y) for x, row in enumerate(matrix) for y, val in enumerate(row) if val == 1]
    tetramino[0] = new_coords
    tetramino[2] = (0, 0)
    return tetramino


def placer(tetramino, grid):
    new_grid = [row[:] for row in grid]
    new_tet=tetramino
    coords = new_tet[0]
    color = new_tet[1]
    offset = new_tet[2]
    collision=False
    if offset[0]<0 :
        coords = sorted(coords, key=lambda coord: coord[0])
        nb=som(coords,True)
    if offset[0]>0:
        coords = sorted(coords, key=lambda coord: coord[0], reverse=True)
        nb=som(coords,True)
    if offset[1]<0:
        coords = sorted(coords, key=lambda coord: coord[1])
        nb=som(coords,False)
    if offset[1]>0:
        coords = sorted(coords, key=lambda coord: coord[1], reverse=True)
        nb=som(coords,False)
    if(offset[1]==offset[0] and offset[0]==0):
        coords = sorted(coords, key=lambda coord: coord[0])
        nb=som(coords,True)
    new_coords = []
    for coord in coords:

        x,y = (coord[0] + offset[0]), (coord[1] + offset[1])
        next_etape=(x,y)
        
        if (
            (x==len(grid[0])-1) or 
            (y==len(grid)-1) or 
            (x==-1) or 
            (y==-1)
            ):
            collision=True
            break
        if not(
            (new_grid[coord[1]][coord[0]-1]=="--" and new_grid[coord[1]+1][coord[0]]=="| ") or
            (new_grid[coord[1]][coord[0]-1]=="--" and new_grid[coord[1]-1][coord[0]]=="| ") or 
            (new_grid[coord[1]][coord[0]+1]=="--" and new_grid[coord[1]+1][coord[0]]==" |") or
            (new_grid[coord[1]][coord[0]+1]=="--" and new_grid[coord[1]-1][coord[0]]==" |") ) :
            if ( (new_grid[next_etape[1]][next_etape[0]]=='--' or new_grid[next_etape[1]][next_etape[0]]==' |' or new_grid[next_etape[1]][next_etape[0]]=='| ')):
                new_coords = []
                for coord in coords:
                    etape=(coord[0]+ offset[0]*nb,coord[1]+ offset[1]*nb)
                    new_coords.append(etape)
                    if (new_grid[coord[1]+ offset[1]*nb][coord[0]+ offset[0]*nb]=="--" or
                        new_grid[coord[1]+ offset[1]*nb][coord[0]+ offset[0]*nb]=="| " or 
                        new_grid[coord[1]+ offset[1]*nb][coord[0]+ offset[0]*nb]==" |" or
                        new_grid[coord[1]+ offset[1]*nb][coord[0]+ offset[0]*nb]!="  " 
                        ):
                        collision=True
                        break
                       
                    
    
                    
                break
        
        if new_grid[y][x] == "  " or next_etape in coords     :
            new_coords.append(next_etape)
        else:
            new_coords.append(next_etape)
            collision = True
            break
    if not collision:
        for coord in coords:
            x, y = coord
            new_grid[y][x] = "  "

        new_tet[0] = new_coords

        for coord in new_coords:
            x, y = coord
            new_grid[y][x] = color

        return create_bar(new_grid), new_tet
    else:
        os.system('cls')
        display_x(new_grid,new_tet[0],new_coords,color)
        for i in range(10000000):
            i=i+1
        return grid, tetramino
def display_x(grid,or_tet,fk_tet,color):
    for coord in or_tet:
        x, y = coord
        grid[y][x] = "  "

    p=color.find("m")

    for coord in fk_tet:
        x, y = coord
        grid[y][x] = color[:p+1]+"X"+color[p+2:]
    display_grid(grid)


def tet_colorize(tet):
    for i in range(1,len(tet)):
        tet[i][1]=colorize_text(str(i), tet[i][1])
    return tet
def colorize_text(text, color_code):
    text=text + ' '
    return f'\x1b[{color_code}m{text}\x1b[0m'

def setup_tetraminos(tetraminos, grid):
    w=(len(grid[0])-2)//3
    h=(len(grid)-2)//3
    for indx,i in enumerate(tetraminos):
        if i ==['.',(0,0)]:
            continue
        coords=i[0]
        grid_color_code = i[1]
        for jndx,j in enumerate(coords):
            j=list(j)
            x,y=j
            if(indx in [1, 2, 3]):
                if indx == 1:
                    grid[y][x] = i[1]=colorize_text(str(indx), grid_color_code)

                elif indx == 2:
                    grid[y][x + w] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[0]=x+w
        
                elif indx == 3:
                    grid[y][x + w * 2 + 2] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[0]=x+w*2+2
            if(indx in [4, 5]):
                if indx == 4:
                    grid[y + h][x] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[1]=y+h
                if indx == 5:
                    grid[y + h][x + w * 2 + 2] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[1]=y+h
                    j[0]=x+w*2+2
            if(indx in [6, 7, 8]):
                if indx == 6:
                    grid[y + h * 2 + 2][x] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[1]=y+h*2+2
                if indx == 7:
                    grid[y + h * 2 + 2][x + w] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[1]=y+h*2+2
                    j[0]=x+w
                if indx == 8:
                    grid[y + h * 2 + 2][x + w * 2 + 2] =i[1]=colorize_text(str(indx), grid_color_code)
                    j[1]=y+h*2+2
                    j[0]=x+w*2+2
            j=tuple(j)
            coords[jndx]=j 
        i[0]=coords
    return grid,tetraminos
def maximaze_tet(tet,dimensions,indc):
    w,h=dimensions
    coords=tet[0]
    for i,coord in enumerate(coords):
        coord=list(coord)
        x,y=coord
        if indc==1:
            x=x
            y=y
        elif indc==2:
            x=x + w
            y=y
        elif indc==3:
            x=x+w*2+2
            y=y
        elif indc==4:
            y=y+h
            x=x
        elif indc==5:
            y=y + h
            x=x + w * 2 + 2
        elif indc==6:
            y=y + h * 2 + 2
            x=x
        elif indc==7:
            y=y + h * 2 + 2
            x=x + w
        elif indc==8:
            y=y+h*2+2
            x=x+w*2+2
        coord=x,y
        coord=tuple(coord)
        coords[i]=coord
    tet[0]=coords
    return tet  
def display_win(w,h,grid,tst):
    grid = [["  "] * (3 * w + 2) for _ in range(3 * h + 2)]
    x = len(grid[0])//2
    y=len(grid)//2
    if(tst):
        ch="    WINNER    "
        grid[x][y]=colorize_text(ch,"0;105")
    display_grid(grid)
def display_grid(grid):
    for row in grid:
        print(''.join(row))
def config_tetraminos(data,decale):

    coordinates_string = data[0]
    coordinates_list = [tuple(map(int, coord.strip('()').split(','))) for coord in coordinates_string.split(';')]
    result_list = [coordinates_list, data[1], decale]
    return result_list
def cls_old(tet,grid):
    coords=tet[0]
    for coord in coords:
        x,y=coord
        grid[y][x]="  "
    return grid
def main(file_path):
    dimensions, tetraminos = import_card(file_path)
    width, height = dimensions
    for i in range(len (tetraminos)):
        if tetraminos[i] ==['.',(0,0)]:
            continue

        tetraminos[i] = config_tetraminos(tetraminos[i], (0, 0))
    grid = create_grid(width, height)
    tet_rotate = copy.deepcopy(tetraminos)   
    tet_rotate=tet_colorize(tet_rotate) 

    grid,tetraminos=setup_tetraminos(tetraminos, grid)

    os.system('cls')
    display_grid(grid)
    x=''
    while True:
        key = getkey()
        key = key.decode('utf-8')
        if key.isdigit() and 1 <= int(key) <= 6:
            x=int(key)
            print(tetraminos[x])
        if key.lower() == 'i' and x!='':
            if (0,-1) not in tetraminos[x]:
                tetraminos[x][2]=(0,-1)
            grid,tetraminos[x] = placer(tetraminos[x], grid)
        elif key.lower() == 'k' and x!='':
            if (0,1) not in tetraminos[x]:
                tetraminos[x][2]=(0,1)
            grid,tetraminos[x] = placer(tetraminos[x], grid)
        elif key.lower() == 'j' and x!='':
            if (-1,0) not in tetraminos[x]:
                tetraminos[x][2]=(-1,0)
            grid,tetraminos[x] = placer(tetraminos[x], grid)
        elif key.lower() == 'l' and x!='':
            if (1,0) not in tetraminos[x]:
                tetraminos[x][2]=(1,0) 
            grid,tetraminos[x] = placer(tetraminos[x], grid)
        elif key.lower() == 'o' and x!='':
            grid=cls_old(tetraminos[x], grid)
            tetraminos[x]=rotate_tetramino(tet_rotate[x], clockwise=False)
            new = copy.deepcopy(tet_rotate[x]) 
            print(tetraminos[x])
            tet_rotate[x]=maximaze_tet(tetraminos[x],dimensions,x)
            print(tetraminos[x])
            grid,tetraminos[x] = placer(tetraminos[x], grid)
            tet_rotate[x]=new
            print(tetraminos[x])
        elif key.lower() == 'u' and x!='':
            grid=cls_old(tetraminos[x], grid)
            tetraminos[x]=rotate_tetramino(tet_rotate[x], clockwise=False)
            new = copy.deepcopy(tet_rotate[x]) 
            print(tetraminos[x])

            tetraminos[x]=maximaze_tet(tetraminos[x],dimensions,x)
            print(tetraminos[x])
            grid,tetraminos[x] = placer(tetraminos[x], grid)
            tet_rotate[x]=new
            print(new)
        elif key.lower() == 'v':
            if(check_win(width, height,grid)):
                os.system('cls')
                display_win(width, height,grid,True)

        else:

            print("Invalid input. Please enter a valid key.")
        os.system("cls")
        display_grid(grid)
        


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tetramino.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)