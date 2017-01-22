import numpy as np
from sklearn.naive_bayes import GaussianNB

def main():
    #   features, values
    x = np.array(
        [
            [88.5,  85.2,   84.7,   86,     84.58   ],
            [87.3,  83,     81,     88,     81      ],
            [24.6,  9.7,    14.8,   54.8,   14.76   ],
            [23,    14,     14,     54,     12      ],
            [52.09, 60.69,  43.04,  55.5,   40.61   ],
            [54,    71,     50,     94,     46      ]
        ]
    )
    #   label
    y = np.array(['b','b','c','c','d','d'])

    clf = GaussianNB()
    clf.fit(x, y)

    print( "Prediction!!!!!!")
    print( clf.predict(
        [
            [75.5, 83.9, 60.8, 88.5, 82.3],
            [20,4,11,53,7],
            [28,80,23,52,23],
            [86,84,83,85,84]
        ]
    ))
    print( "Done Bitch!!")

if __name__ == "__main__":
    main()
