#include "lattice.h"

Lattice::Lattice(int n) : n{n} {
    // seed random number generator with "true" randomness
    random_device rd;
    generator.seed(rd()); 

    // iterate through lattice and set random spin
    for (int i = 0; i < n; i++) {
        grid.push_back(vector<int>(n));
        for (int j = 0; j < n; j++) {
            grid[i][j] = (bool_distr(generator)) ? 1 : -1;
        }
    }
}

int Lattice::get_spin(int row, int col) {
    return grid[row][col];
}

int Lattice::get_spin(tuple<int, int> row_col) {
    return grid[get<0>(row_col)][get<1>(row_col)];
}

void Lattice::flip_spin(tuple<int, int> row_col) {
    // -1 -> 1 and 1 -> -1
    grid[get<0>(row_col)][get<1>(row_col)] = (get_spin(row_col) == 1) ? -1 : 1; 
}

tuple<int, int> Lattice::choose_random_spin() {
    return make_tuple(int_distr(generator), int_distr(generator));
}

double Lattice::calculate_energy(tuple<int, int> row_col) {
    int row = get<0>(row_col);
    int col = get<1>(row_col);

    /* adding neighbours spin together in i,
       wrapping for periodic boundary conditions,
       multiplying answer with -1 depending on state of center spin */

    double i = 0.0;
    i += (get_spin((row + 1) % n, col) == 1) ? 1.0 : -1.0;
    i += (get_spin((n + ((row - 1) % n)) % n, col) == 1) ? 1.0 : -1.0;
    i += (get_spin(row, (col + 1) % n) == 1) ? 1.0 : -1.0;
    i += (get_spin(row, (n + ((col - 1) % n)) % n) == 1) ? 1.0 : -1.0;
    if (get_spin(row_col) == -1) {
        i *= -1.0;
    }

    return i;
}

ostream& operator<<(ostream& out, Lattice& l) {
    for (int i = 0; i < l.n; i++) {
        for (int j = 0; j < l.n; j++) {
            out << l.get_spin(i, j) << " ";
        }
        out << "\n";
    }
    return out;
}
