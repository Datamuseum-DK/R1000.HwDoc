#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

'''
    Initial image processing:

        Crop a bit outside the thik boundary

        Locate corners of thick boundary

        Locate corners of thin boundary

        Locate arrows between boundaries

        locate doc-box
'''

# Finagle Constants for individual images

FINAGLE_PAGES = {
    "FIU": {
        "0045": { "no_right_arrows": True},
    },
    "TYP": {
        "0031": { "no_right_arrows": True},
        "0037": { "no_right_arrows": True},
    },
    "VAL": {
    },
    "IOC": {
        "0063": {
             "no_left_arrows": True,
             "coarse_right": 5610,
             "e_t_l":   (147, 71),
             "e_t_r":   (96, 6196),
             "e_b_l":   (4159, 115),
             "e_b_r":   (4116, 6236),
             "i_t_l":   (213, 160),
             "i_t_r":   (150, 6138),
             "i_b_l":   (4097, 160),
             "i_b_r":   (4062, 6177),
        },
    },
    "RESHA": {
    },
}

FINAGLE_LANDMARKS = {
    "RESHA": {
        "0002": (
            (1074, 3716, 11.1, 13.8, "manual"),
            (1630, 2170,  9.1,  8.0, "manual"),
            ( 318,  894, 14.1,  3.2, "manual"),
        ),
        "0003": (
            (1134, 1772, 10.9,  6.5, "manual"),
        ),
        "0004": (
            (1396, 2605, 9.8,  9.6, "manual"),
            (1394, 4186, 9.8, 15.5, "manual"),
        ),
    },
}
