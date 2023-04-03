DROP DATABASE IF EXISTS Syllabus_management_system;
CREATE DATABASE Syllabus_management_system;
USE Syllabus_management_system;

CREATE TABLE user_details (
	account_ varchar(30) not null,
    password_ varchar(20) not null
);

CREATE TABLE major (
	major_id varchar(20) not null,
	major_name varchar(50) not null,
    primary key (major_id) 
);

CREATE TABLE course (
	course_id varchar(20) not null,
    course_name long varchar,
    credit_points_inECTs int,
    background_knowledge long varchar,
    textbook long varchar,
    ref_literature long varchar,
    course_content long varchar,
    objectives long varchar,
    primary key (course_id)
);

CREATE TABLE major_course (
	major_id varchar(20) not null references major(major_id),
	course_id varchar(20) not null references course(course_id)
);

CREATE TABLE time_commitment_inHOURS (
	course_id varchar(20) not null,
    lecture int,
    tutorial int,
    practical int,
    total int,
    primary key (course_id)
);

CREATE TABLE assessment_percent (
	course_id varchar(20) not null,
    attendance int,
    exercise int,
    assignment int,
    report int,
    midterm int,
    final int,
    primary key (course_id)
);

CREATE TABLE syllabus(
	id int, 
	major_id varchar(20) not null, 
	course_name long varchar , 
	credit_points_inECTs int,
	background_knowledge long varchar, 
	textbook long varchar, 
	ref_literature long varchar,
	course_content long varchar, 
	objectives long varchar, 
	lecture int, 
	tutorial int, 
	practical int, 
	attendance int, 
	exercise int, 
	assignment int, 
	report int, 
	midterm int, 
	final int
);

INSERT INTO syllabus (id, major_id, course_name, credit_points_inECTs, background_knowledge, textbook, ref_literature, course_content, objectives, lecture, tutorial, practical, attendance, exercise, assignment, report, midterm, final) VALUES 
(1, "CS", "PROBABILITIES & STATISTICS", 4, "Analysis, Integration and ODE", "[1].Spiegel R. M., Schiller J., Srinivasan R. A., Probability and Statistics, Third edition, McGraw Hill, 
2009. [2].Montgomery C. D., Runger C. G., Applied Statistics and Probability for Engineers, Fifth edition, John Wileys& Sons, 2011.", "[1].Course notes, in-class exercises and homework problems. 
[2].Spiegel R. M., Schiller J., Srinivasan R. A., Probability and Statistics, Third edition, McGraw 
Hill, 2009. 
[3].Montgomery C. D., Runger C. G., Applied Statistics and Probability for Engineers, Fifth 
edition, John Wileys& Sons, 2011. 
[4].Vidakovic B., Statistics for Bioengineering Sciences, Springer 2011.", "Basic Probability; Random Variables and Probability Distributions; Mathematical Expectation; Special Probability Distributions; Sampling Theory; Estimation Theory; Tests of Hypotheses and Significance; Curve Fitting, Regression, and Correlation; Analysis of Variance; Nonparametric Tests", 
"1. Ability to manipulate sets and events, use axioms of probability, computer probabilities of events & solve counting problems.
2. Ability to generate random variables from experiments, use probability distribution and density 
functions, use common distributions and computer statistical quantities random variables and 
random vectors.
3. Ability to determine the distributions and statistical quantities of random variables, to apply limit 
theorems.
4. Ability to understand basic statistical concepts, random sampling, statistical inference, to 
regression and correlation.
5. Ability to construct point estimation, confidence and prediction intervals.
6. Ability to test hypotheses
7. Ability to perform Analysis of Variance.", 25, 15, 0, 10, 10, 0, 0, 30, 50),

(2, "CS", "ANALYSIS & ALGEBRAIC STRUCTURES", 3, "Math reasoning, expansions of the function into series", "[1] W. F. Trench, Introduction to real analysis (Available online). [2] Milner, Group theory, Lecture notes, 2003 (Available online for personal use)", "[1].G.Cain, J.Herod: Multivariable calculus, 1997.
[2].W. F. Trench, Introduction to real analysis (Available online)
[3].Milner, Group theory, Lecture notes, 2003 (Available online for personal use)
[4].Gedder et al., Algorithms for computer algebra, Kluwer Academic Publishers, 1992.", "Calculus of several variables: The limits, continuity of functions; The differentiability; The integration technics; Applications. Algebraic structures: Basic definitions; Semi groups as the flows; Groups acting on the sets; Computer algebra", 
"Basic understanding of how the multivariate calculus differs from 1D case: the double limits, 
continuity, partial derivatives, integration over the domain and curvilinear integrating technics. 
Students should be able to be familiar with some applications in the optimization problem and 
graphing visualization. Many new algebraic concepts will be introduced in the relations with ICT 
branch’ preparation: the learners should be known about the built-in structures in the networking 
basing on partitions, filters ordering of the most simple PC’ data processing.", 20, 16, 0, 5, 5, 0, 0, 20, 70),

(3, "ICT ", "ALGORITHMS AND DATA STRUCTURES", 3, "Programming languages (C), Mathematics", "[1]Adam Drozdek, Data Structures and Algorithms in C++, 4th Edition, Cengage Learning, 2012", "[1] Adam Drozdek, Data Structures and Algorithms in C++, 4th Edition, Cengage Learning, 2012", "1. Basic Programming Concepts in C++
2. Elementary Data Structures 
3. Abstract (Linear) Data Types I
4. Abstract (Linear) Data Types II
5. Recursive Algorithms
6. Trees
7. Sorting Algorithm I
8. Sorting Algorithm II
9. Searching Algorithm
10. Graphs", 
"- Understand the basic programming concepts
- Understand analysis and design of computer algorithm and data structures
- Analyze real-world problems and design appropriate data structures according to the problems using techniques from the course, Work individually or in a group", 20, 0, 16, 10, 0, 30, 0, 0, 60),

(4, "ICT", "OBJECT-ORIENTED PROGRAMMING", 3, "
- Understand fundamental concepts of programming 
- Basic data types, array, string, pointer, etc,
- Basic algorithms such as sorting, searching, etc 
- Have good programming style (e.g. comments, indentation, naming, etc)", "[1] Kathy Sierra, Bert Bates, Head First Java, 2nd Edition, O' Reilly, 2005. [2] Deitel & Deitel, Java How to Program, 9th Edition, Prentice Hall, 2011.", "[1].Kathy Sierra, Bert Bates, Head First Java, 2nd Edition, O' Reilly, 2005.
[2].Deitel&Deitel, Java How to Program, 9th Edition, Prentice Hall, 2011.
[3]. Java™ Platform, Standard Edition 7 API Specification, 
http://docs.oracle.com/javase/7/docs/api/index.", "1. Course introduction - Introduce to Object-oriented programming
2. Introduction to Java programming language
3. Objects and classes - Instance variables and methods – Encapsulation
4. Objects and object references
5. Class members vs. Instance members - Java packages
6. Inheritance - Polymorphism
7. Assignment 1 presentation
8. Abstraction
9. Interfaces
10. Exceptions
11. Data structures
12. I/O Streams
13. Principles of object-oriented design
14. Assignment 2 presentation", 
"- Understand the basic principles and concepts of object-oriented programming
- Practice how to use these concepts and principles with Java programming language 
- Apply object-oriented techniques to develop computer programs", 25, 0, 15, 10, 0, 20, 0, 0, 50);

SELECT * FROM syllabus;
