**Markov Distinction**
-

This project uses a Markov chain to draw an original image based on a given image.

**Usage**
-
Install the necessary requirements and run: 
- pip install pillow
- python main.py

**Meaning**
-
This project is in some ways a synthesis of a number of classes I have taken.
In intermediate linear algebra, I explored Markov chains both with mathematical formality and through examples such as
Google's PageRank. The approach used to count occurrences of pixel colors is very similar to both a Data Structures lab
and a project in the aforementioned linear algebra class where I represented books as vectors. Most recently, in nature-inspired
computation,  we examined a number of algorithms which, on the whole, tried to balance "greediness" and "randomness." This
project, and computational creativity in general, seem to follow along a similar path; this is expressed well in the distinction
between phenotype and genotype in our assigned reading.

**Challenge**
- 
This project challenged me most with its vagueness. Coming from a software engineering internship,
I am used to not only having clear requirements, but understanding the end goal of a change (that is, if I need to ask for
clarification, I can within the context of the overarching project). I probably should have sought more clarification about this 
project, but given these differences, I wasn't sure what questions to ask. Moving forward, it's clear that I should 
cast aside my old expectations not be hesitant to seek answers.

**Creativity**
- 
While the evaluation of _any_ system's being creativity is probably beyond the scope of this assignment,
I think there are ways in which this system can legitimately be called creative, at least insofar as it mirror human creativity.
A human being can observe the world around them, store these observations as information, and then make "creative" decisions based on it.
This system observes an image, stores the observations in a Markov chain of colors and their neighbors, and subsequently generates an image.
A human may not count pixels in this way, but the experiential nature of learning is, at the very least, analogous to the way this system learns.
The simple fact that we can understand what the machine is doing here while we might not understand completely the neuroscience of human creativity does
not preclude this system from being creative.

**Sources**
-
https://jonnoftw.github.io/2017/01/18/markov-chain-image-generation (a similar approach)
