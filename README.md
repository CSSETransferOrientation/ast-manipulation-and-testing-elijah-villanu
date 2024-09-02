### What Was Done
   The sections of the project that I have finished are the additive identity (x + 0 = x), multiplicative identity (x * 1 = x), and the multiply by zero identity (x * 0 = 0). However, they only work partially in certain test cases. The errors appear if the simplify binops is only run once, or each identity is only run once. I resolve this issue (up to a certain level of the tree) simply by calling the method twice, but I believe the issue lies in the order of the call and what takes priority (Example: multiply by zero first before multiply by one).

### Learned + Experienced
   Some things that I found the most useful to learn in this lab were getting used to classes in python and learning about (although not fully able to implement) regression testing. Coming from a Java background, transitioning to python classes felt odd especially with syntax and how things are contained in a single file. For testing, the lab showed the importance of strategizing which tests will really show the vulnerabilites of your code. Choosing the right tests and edge cases are skills I will continue to improve upon.

 ### Difficult Bug
   The biggest issues I ran into, as probably seen by running the code, is that I was not able to get the test bench to work. As mentioned before, my identities work with certain test cases, but I am only aware of it's functionality through the old ways of testing (simple printing as seen as a commented out block of code all the way down). The errors unittest was throwing out was with how I was using the file to initialize the BinOpAst class (line 30). As of now, I am unsure how to resolve this. 

;;> So there looks like there are some errors in your tests, which was probably confusing you. However, you should really test one thing at a time to narrow down the potential issues. See your code for more comments.
;;> Overall this was a great start and you had it most of the way there!
