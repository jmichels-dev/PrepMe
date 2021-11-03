    The first step to implementing PrepMe was repurposing code from CS50 Finance into code that I could use for PrepMe. The mainly consisted of getting rid of things that I
didn't need from Finance. I also used the login function and pages, as well as the navbar to give my website a solid foundation. The registration page was taken from Finance,
but I wanted to display errors that the user could read and have a chance to fix, rather than the Apology that was implemented, which would redirect the user to a whole new page
to tell them what the issue was. This is why I decided to pass an array of the usernames to JavaScript, so it would detect if a username was already taken, rather than with Apology,
which checked after the form was submitted. All of the other possible errors with register and the rest of PrepMe also use alerts, and will not allow the user to submit the form
until these errors are resovled. This method of error notification and resolution seemed more practical to me and also more user-friendly, since they won't have to reload a page
every time they make an error.
    After this, I determined the most clean way to show the user their classes, tests, and recommendations was to use tables with alternating background colors. It also made the most
sense to implement a separate page to edit each table, rather than allowing the user to edit them all at once. This is because the latter method would have proved to be very difficult
and likely messy, since any changes need to be recorded in prepme.db in order for the user to see the changes take effect. As for the edit pages themselves, I tried to limit the variability
of user inputs as much as possible, since variability leads to a greater chance of errors and bugs occurring. For the test editing page, I made different fields for users to input information
based on the test they selected, due to the different scores that are pertinent to each exam. For example, the only information PrepMe requires for an ACT is the score, however if the user selects
ACT w/ Writing, an input field appears asking for the writing score as well. I did allow freedom of naming classes and recommenders, since ultimately those values don't matter when rating the
user's application. I want PrepMe to have function as both an application rater as well as an organization tool for future applicants, which is why some values in the tables are not used in the
rating algorithm; they are there just to provide more clarity for the user.
    The rating algorithm uses the values that the user inputs in order to determine the overall rating of the user's application. It bases its rating off of things as simple as how many core-classes
the user has taken or how strong their recommendations are to more complicated things such as the number of honors classes they have taken or if they have taken any SAT Subject Tests. While not all,
a large amount of the data the user inputs is used in the rating algorithm, and so there is a large variability of responses that a user can get when they look at their application rating. For example,
the algorithm has six separate possible outcomes based on the user's test score, and so this specificity across all of the values used for the rating algorithm really makes it seem like PrepMe is a personal
help tool rather than a website that a large amount of people use.
    As for the overall rating of the application, the algorithm uses a counter that ticks up each time the algorithm detects an issue or weakness with the user's application. At the end, the higher the
counter, the weaker the application is deemed to be. Some weaknesses are obviously worse than others, and so each weakness has been assigned a weight in terms of how much will be added to the counter.
Weaknesses that greatly diminish the strength of a user's application, add more to the counter than those that are relatively minor. ACT and SAT test scores and essay scores were converted to values on
the same scale using official score concordance tables, so that they could be compared to each other more easily and the algorithm could then determine the highest of those scores. The overall rating
as well as the entire rating algorithm is successful, because it can point out weaknesses in a wide variety of applications, allowing users to clearly see areas in which they can improve.
    The resume tips page was implemented because I know that a lot of applicants submit resumes, and it can be difficult to find out what a resume that a college student would submit looks like.
I provided a physical example of what I thought was a good college resume, and also some tips to keep in mind when writing a student resume. This gives my site another purpose, and another reason for
users to use it. Finally, the about me page was implemented because I wanted to humanize myself to my users, and show them that I was in the same spot as they were not long ago. It serves to
build a relationship with my users and this relationship encourages more use of the site.