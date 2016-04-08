#include <iostream>

// By no means is this good C++, pretty much just a straight up syntax swap from the python version.

class Dice
{
    public:
        int up;
        int down;
        int north;
        int south;
        int west;
        int east;

        Dice()
        {
            up = 0;
            down = 0;
            north = 0;
            south = 0;
            west = 0;
            east = 0;
        }

        void tip_west()
        {
            int old_west = west;
            west = up;
            up = east;
            east = down;
            down = old_west;
        }

        void tip_east()
        {
            int old_east = east;
            east = up;
            up = west;
            west = down;
            down = old_east;
        }

        void tip_north()
        {
            int old_north = north;
            north = up;
            up = south;
            south = down;
            down = old_north;
        }

        void tip_south()
        {
            int old_south = south;
            south = up;
            up = north;
            north = down;
            down = old_south;
        }
};


class Solver
{
    int dim_x, dim_y;
    int max_x, max_y;
    int x, y;

    int* grid;
    bool* visited;

    Dice dice;

    double max_score;

    public:
    Solver(int* _grid, int _dim_x, int _dim_y) : x(0), y(0), max_x(dim_x - 1), max_y(dim_y - 1), dim_x(_dim_x), dim_y(_dim_y)
    {
        grid = _grid;

        visited = new bool[dim_x * dim_y];
        for(int i = 0; i < dim_x * dim_y; ++i)
            visited[i] = false;
    }

    ~Solver()
    {
        delete [] visited;
    }


    double solve()
    {
        solve_recursive(0, 0, 1);
        return max_score;
    }

    int grid_index(int x, int y)
    {
        return dim_y * x + y;
    }

    private:
    bool is_good_move(int dice_value, int grid_value)
    {
        if(dice_value == 0 || grid_value == 0 || dice_value == grid_value)
            return true;
        return false;
    }

    void solve_recursive(int x, int y, double product)
    {
        bool grid_modified = false;
        bool dice_modified = false;

        if(dice.up == 0 && grid[grid_index(x,y)] != 0)
        {
            dice.up = grid[grid_index(x,y)];
            dice_modified = true;
        }
        else if(dice.up != 0 and grid[grid_index(x,y)] == 0)
        {
            grid[grid_index(x,y)] = dice.up;
            grid_modified = true;
        }
        else if(dice.up == 0 and grid[grid_index(x,y)] == 0)
        {
            for(int i = 1; i < 10; ++i)
            {
                grid[grid_index(x,y)] = i;
                solve_recursive(x, y, product);
            }
            grid[grid_index(x,y)] = 0;
            return;
        }
        else if(grid[grid_index(x,y)] != dice.up)
            return;

        product *= grid[grid_index(x,y)];

        if(x == max_x && y == max_y)
        {
            if(product > max_score)
                max_score = product;
        }
        else
        {
            visited[grid_index(x,y)] = true;

            if(x < max_x && !visited[grid_index(x+1,y)])
            {
                if(is_good_move(dice.north, grid[grid_index(x+1,y)]))
                {
                    dice.tip_south();
                    solve_recursive(x + 1, y, product);
                    dice.tip_north();
                }
            }
            if(x > 0 && !visited[grid_index(x - 1,y)])
                if(is_good_move(dice.south, grid[grid_index(x - 1, y)]))
                {
                    dice.tip_north();
                    solve_recursive(x - 1, y, product);
                    dice.tip_south();
                }
            if(y < max_y && !visited[grid_index(x, y + 1)])
            {
                if(is_good_move(dice.west, grid[grid_index(x, y + 1)]))
                {
                    dice.tip_east();
                    solve_recursive(x, y + 1, product);
                    dice.tip_west();
                }
            }
            if(y > 0 && !visited[grid_index(x, y - 1)])
            {
                if(is_good_move(dice.east, grid[grid_index(x, y - 1)]))
                {
                    dice.tip_west();
                    solve_recursive(x, y - 1, product);
                    dice.tip_east();
                }
            }
        }

        //Undo stuff to avoid copying
        visited[grid_index(x,y)] = false;
        if(grid_modified)
            grid[grid_index(x,y)] = 0;
        if(dice_modified)
            dice.up = 0;
    }
};


int main()
{
    const int tiny_dim = 2;
    int tiny_grid[tiny_dim * tiny_dim] = {6, 2, 3, 4};
    int tiny_grid_with_hole[tiny_dim * tiny_dim] = {6, 2, 0, 4};

    const int small_dim = 5;
    int small_grid[small_dim * small_dim] = {3, 4, 1, 7, 5, 1, 2, 4, 3, 5, 2, 4, 3, 6, 2, 9, 5, 7, 2, 3, 5, 8, 3, 4, 1};

    const int full_dim = 12;
    int full_grid[full_dim * full_dim] = {1, 5, 4, 4, 6, 1, 1, 4, 1, 3, 7, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 6, 4, 1, 8, 1, 4, 2, 1, 0, 3, 7, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 1, 0, 6, 1, 6, 2, 0, 2, 0, 1, 8, 0, 4, 0, 1, 0, 0, 8, 0, 3, 0, 5, 4, 0, 2, 0, 5, 0, 0, 3, 0, 5, 0, 2, 8, 0, 5, 0, 1, 1, 2, 3, 0, 4, 0, 6, 6, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 6, 3, 0, 6, 3, 6, 5, 4, 3, 4, 5, 0, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 6, 6, 4, 5, 2, 1, 1, 1, 7, 1};

    const int stripped_dim = 8;
    int stripped_grid[stripped_dim * stripped_dim] = {6, 4, 1, 8, 1, 4, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 6, 1, 6, 2, 0, 2, 4, 0, 1, 0, 0, 8, 0, 3, 2, 0, 5, 0, 0, 3, 0, 5, 5, 0, 1, 1, 2, 3, 0, 4, 1, 0, 0, 0, 0, 0, 0, 3, 6, 3, 6, 5, 4, 3, 4, 5};



    Solver solver(full_grid, full_dim, full_dim);
    std::cout << solver.solve() << std::endl;

    return 0;
}
