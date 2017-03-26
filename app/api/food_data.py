# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=line-too-long

ingredients = [\
      {\
        "id": 1, \
        "name" : "Tomato", \
        "image": "https://bonnieplants.com/wp-content/uploads/better-bush-tomato.jpg", \
        "recipes": [1, 2, 3], \
        "grocery_items": [], \
        "tags": [2]\
      }, \
      {\
        "id": 2, \
        "name" : "Cheddar Cheese", \
        "image": "https://c2.staticflickr.com/4/3778/11893492083_ce613d2892_b.jpg", \
        "recipes": [1], \
        "grocery_items": [], \
        "tags": [2, 3]\
      }, \
      {\
        "id": 3, \
        "name" : "Butter", \
        "image": "https://c1.staticflickr.com/5/4084/5020808475_809a3cc560_b.jpg", \
        "recipes": [1], \
        "grocery_items": [], \
        "tags": [2]\
      }, \
      {\
        "id": 4, \
        "name" : "Bacon", \
        "image": "https://c2.staticflickr.com/4/3603/3603122710_6ea3b5447c_z.jpg?zz=1", \
        "recipes": [2, 3], \
        "grocery_items": [1], \
        "tags": [1]\
      }, \
      {\
        "id": 5, \
        "name" : "Lettuce", \
        "image": "https://c1.staticflickr.com/3/2866/9054249842_a0108e22ff_c.jpg", \
        "recipes": [2, 3], \
        "grocery_items": [], \
        "tags": [2, 3]\
      }, \
      {\
        "id": 6, \
        "name" : "Mayonnaise", \
        "image": "https://c2.staticflickr.com/4/3205/3048070242_305d588993_z.jpg", \
        "recipes": [2, 3], \
        "grocery_items": [], \
        "tags": [2, 3]\
      }, \
      {\
        "id": 7, \
        "name" : "Turkey Breast Sandwich Meat", \
        "image": "https://img.clipartfest.com/4b0880d59be58ff4bb1c84ce5957888d_gc52y6axltth-jzlkzq6hfhwn-turkey-lunch-meat-clipart_1280-960.jpeg", \
        "recipes": [2], \
        "grocery_items": [2], \
        "tags": [2]\
      }, \
      {\
        "id": 8, \
        "name" : "Avocado", \
        "image": "https://c1.staticflickr.com/9/8433/29424695541_29288edfd2_c.jpg", \
        "recipes": [], \
        "grocery_items": [], \
        "tags": [1, 2]\
      }, \
      {\
        "id": 9, \
        "name" : "Bread", \
        "image": "https://c1.staticflickr.com/1/647/33323504266_93ae1664a0_c.jpg", \
        "recipes": [1, 2, 3], \
        "grocery_items": [3], \
        "tags": [2]\
      }\
    ]

recipes =\
    [\
      {\
        "id": 1, \
        "name": "Grilled Cheese with Tomato", \
        "image": "http://akns-images.eonline.com/eol_images/Entire_Site/2013424/rs_1024x759-130524141502-1024.GrilledCheeseTomato.ms.052413.jpg", \
        "blurb": "A cheese and tomato sandwich makes a healthy lunch option, especially when paired with a side salad.", \
        "instructions": "Directions: Spread both slices of bread with a light layer of mayo. Put slice of cheese on one piece of bread. Add tomato slices. Cover tomato slices with other slice of cheese, then cover with other piece of bread. In the meantime, heat griddle or pan with butter. Also spread butter on top of each side of bread. Grill until sandwich is brown on both sides and cheese is melted.", \
        "ingredient_amount":\
          [\
            {\
              "ingredient_id": "3", \
              "amount": 1.0, \
              "unit": "stick", \
              "original_string": "1 stick plus 2 tablespoons butter"\
            }, \
            {\
              "ingredient_id": "1", \
              "amount": 2.0, \
              "unit": "slice", \
              "original_string": "2 slices of tomatoes"\
            }, \
            {\
              "ingredient_id": "9", \
              "amount": 2.0, \
              "unit": "slice", \
              "original_string": "2 slices of bread"\
            }\
          ], \
        "tags": [1, 2, 4]\
      }, \
      {\
        "id": 2, \
        "name": "Classic Turkey Club", \
        "image": "http://cdn.boarshead.com/img/_content/recipe/38-classic-turkey-club/detail-001.1465313338.jpg", \
        "blurb": "This sandwich is just what the name says: Classic. An easy recipe with excellent results.", \
        "instructions": "Directions: Toast the bread, on both sides, in a toaster or using the broiler. On a clean surface, place the three slices of bread side-by-side. Spread mayonnaise on one side of each bread slice. Stack the following ingredients in order on the first slice of bread, lettuce, tomato, Monterey Jack Cheese, turkey, bacon and a slice of white bread. Repeat above sequence for the second layer. Finish by topping off with a slice of bread, mayonnaise side down.", \
        "ingredient_amount":\
          [\
            {\
              "ingredient_id": "1", \
              "amount": 3.0, \
              "unit": "slice", \
              "original_string": "3 slices of tomatoes"\
            }, \
            {\
              "ingredient_id": "9", \
              "amount": 3.0, \
              "unit": "slice", \
              "original_string": "3 slices toasted bread"\
            }, \
            {\
              "ingredient_id": "6", \
              "amount": 1.0, \
              "unit": "tbsp", \
              "original_string": "1 tbsp mayonnaise"\
            }, \
            {\
              "ingredient_id": "5", \
              "amount": 2.0, \
              "unit": "slice", \
              "original_string": "2 slices of leaf lettuce"\
            }, \
            {\
              "ingredient_id": "4", \
              "amount": 4.0, \
              "unit": "slice", \
              "original_string": "4 slices of cooked bacon"\
            }, \
            {\
              "ingredient_id": "7", \
              "amount": 5.0, \
              "unit": "slice", \
              "original_string": "5 slices of turkey breast"\
            }\
          ], \
        "tags": [4]\
      }, \
      {\
        "id": 3, \
        "name": "B.L.T.", \
        "image": "http://www.tabletmag.com/wp-content/files_mf/blt_101113_820px.jpg", \
        "blurb": "The basic classic: bacon, lettuce, and tomato -- nothing fancy, just delicious.", \
        "instructions": "Cook the bacon in a large, deep skillet over medium-high heat until evenly browned, about 10 minutes. Drain the bacon slices on a paper towel-lined plate. Arrange the cooked bacon, lettuce, and tomato slices on one slice of bread. Spread one side of remaining bread slice with the mayonnaise. Bring the two pieces together to make a sandwich.", \
        "ingredient_amount":\
          [\
            {\
              "ingredient_id": "1", \
              "amount": 3.0, \
              "unit": "slice", \
              "original_string": "3 slices of tomatoes"\
            }, \
            {\
              "ingredient_id": "9", \
              "amount": 3.0, \
              "unit": "slice", \
              "original_string": "3 slices toasted bread"\
            }, \
            {\
              "ingredient_id": "6", \
              "amount": 1.0, \
              "unit": "tbsp", \
              "original_string": "1 tbsp mayonnaise"\
            }, \
            {\
              "ingredient_id": "5", \
              "amount": 2.0, \
              "unit": "slice", \
              "original_string": "2 slices of leaf lettuce"\
            }, \
            {\
              "ingredient_id": "4", \
              "amount": 4.0, \
              "unit": "slice", \
              "original_string": "4 slices of cooked bacon"\
            }\
          ], \
        "tags": [4]\
      }\
    ]

grocery_items =\
    [\
      {\
        "id": 1, \
        "name": "Kirkland Signature Regular Sliced", \
        "image": "http://i.huffpost.com/gadgets/slideshows/320101/slide_320101_2986024_free.jpg", \
        "upc": "0-75987-67890-5", \
        "ingredient": 4, \
        "tags": [1]\
      }, \
      {\
        "id": 2, \
        "name": "Applegate Naturals Roasted Turkey Breast", \
        "image": "http://happymart.co/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/i/m/img_0880.jpg", \
        "upc": "0-21436-67890-5", \
        "ingredient": 7, \
        "tags": [3]\
      }, \
      {\
        "id": 3, \
        "name": "Ezekiel 4:9 Low Sodium Sprouted Whole Grain Bread", \
        "image": "http://s.eatthis-cdn.com/media/images/ext/437304009/ezekiel-low-sodium-sprouted-bread.jpg", \
        "upc": "0-98875-67890-5", \
        "ingredient": 9, \
        "tags": [3]\
      }\
    ]

tags =\
    [\
      {\
        "id": 1, \
        "name": "Crowd Pleaser", \
        "image": "../static/images/tags/crowd_pleaser.png", \
        "blurb": "This item is sure please nearly everyone. Bring this dish to win the party!", \
        "ingredients": [4, 8], \
        "recipes": [1], \
        "grocery_items": []\
      }, \
      {\
        "id": 2, \
        "name": "Vegetarian", \
        "image": "../static/images/tags/vegetarian.png", \
        "blurb": "These items are for those who choose to eat a semi-plant-based diet. These items will include dishes with egg and dairy products.", \
        "ingredients": [1, 2, 3, 5, 6, 8, 9], \
        "recipes": [1], \
        "grocery_items": []\
      }, \
      {\
        "id": 3, \
        "name": "Great For Sandwiches", \
        "image": "../static/images/tags/sandwichey.png", \
        "blurb": "These items are made to be between two pieces of bread.", \
        "ingredients": [2, 5, 6, 7], \
        "recipes": [], \
        "grocery_items": [2, 3]\
      }, \
      {\
        "id": 4, \
        "name": "Quick!", \
        "image": "../static/images/tags/quick.png", \
        "blurb": "These items can be quickly made for when you're pressed for time. Great for lunches.", \
        "ingredients": [], \
        "recipes": [1, 2, 3], \
        "grocery_items": []\
      }\
    ]
