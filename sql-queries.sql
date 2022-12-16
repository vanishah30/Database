#As a visitor, I want to be able to see a list of auction items (with brief information).
SELECT id,name, SUBSTRING(Description,1,20) FROM autction_object;
#As a visitor, I want to be able to see a detail page per auction item (and see more details).
SELECT * FROM autction_object;

#As a visitor, I want to be able to register a new account and become a user.
insert into user (`email`, `firstname`, `lastname`, `password`) 
values ('victor@nodehill.com', 'Victor', 'Frank', 'hi123');

#As a user, I want to be able to log in.
SELECT email,password FROM user;

#As a user, I want to be able to create new auction items.

INSERT INTO autction_object (Name,Description,start_time,end_time,user)
values ('Microwave','Electrolux brand latest model year 2021','2022-11-12','2022-12-10',14) ;

#As a user, I want auction items to contain at least title, description, start time, end time and image(s).
SELECT Name,description,start_time,end_time,images.url from autction_object
LEFT JOIN images
ON images.object=object;

#7As a visitor, I want to be able to see current bids on auction items in list views
SELECT start_time, end_time,bid.price, autction_object.id from autction_object
LEFT JOIN bid
ON bid.autction_object = bid.id;

#8As a visitor, I want to be able to see the 5 most recent bids on auction items in detail pages.
SELECT * from bid join autction_object on bid.autction_object = autction_object.id where autction_object.id = 5 order by price desc limit 5;

#9As a user, I want to be able to place (higher than current) bids on auction items, on their detail page.
SELECT price, user_id FROM bid WHERE autction_object = 5 ORDER BY price LIMIT 5;
UPDATE bid SET price = 2450 WHERE autction_object = 5;

#10As a user, I should not be able to bid on my own auction items.
SELECT user_id FROM bid WHERE autction_object = 5;   



