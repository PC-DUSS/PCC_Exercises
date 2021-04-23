"""
Pierre-Charles Dussault
March 11, 2021

Random walk with tuple coordinates.
"""
import random


def main():

    # A random walk has already begun. Continue from this position.
    coords_history = [(56, 78), (52, 74), (48, 70), (50, 66)]

    # Take 100 steps.
    for i in range(100):
        x_direction = random.choice([1, -1])
        x_distance = random.choice([0, 1, 2, 3, 4])
        x_step = x_direction * x_distance

        y_direction = random.choice([1, -1])
        y_distance = random.choice([1, 2, 3, 4])
        y_step = y_direction * y_distance

        # Skip steps that don't move at all.
        if x_step == 0 and y_step == 0:
            continue

        # Add the current step to previous coordinates position to find out
        # and store the new position.
        new_x_coord = coords_history[-1][0] + x_step
        new_y_coord = coords_history[-1][1] + y_step

#-------This is another more visual way of doing it.
#       last_coords = coords_history[-1]
#       new_x_coord = last_coords[0] + x_step
#       new_y_coord = last_coords[1] + y_step

        new_coord_tuple = (new_x_coord, new_y_coord)
        coords_history.append(new_coord_tuple)

    print('\nHere is the path you took along your random walk: \n' +
          str(coords_history))


if __name__ == "__main__":
    main()
