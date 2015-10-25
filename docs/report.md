

**How to run new version of simulator**
---------------------------------------

1. To grab new version run ```git pull origin master```
2. To see list of all available options run ```python simulator.py --help```

Basic example:

    python simulation.py --show-total-statistics

    Current time: 1.15248454847
    User Shrek id=Gr9PyGPF forwards message
    Current time: 2.2107178932
    User Shrek id=Gr9PyGPF replies to Iphigenia answer A Beautiful mind
    User Pym id=Fx0Sz4pd forwards message
    Current time: 3.27440983746
    User Janis id=OAX6RTfB forwards message
    Current time: 4.14172636686
    User Houyhnhnm id=ojqWO4RV forwards message
    Current time: 5.04418185058
    User Woolite id=2v8G2RsV forwards message
    Current time: 6.12059652254
    User Tyler id=6E7bFgmf forwards message
    Current time: 7.29005989624
    User Tweedledum id=ClPUgNVk forwards message
    Current time: 8.30030390258
    User Tweedledum id=ClPUgNVk replies to Iphigenia answer Terminator
    User Aquafresh id=ODKK3yl0 forwards message
    Current time: 9.21263450901
    User Timon id=JhEYYoX0 forwards message
    Current time: 10.1521461643
    User Clorox id=shSGLkwa forwards message
    Current time: 11.1523566726
    User Cairo id=guh9BOHW forwards message
    Current time: 12.2589269324
    User Neruda id=xljMYBq5 forwards message
    Current time: 13.2982777243
    User Neruda id=xljMYBq5 replies to Iphigenia answer Matrix
    User Gehrig id=DRqYdvQb forwards message
    Current time: 14.2901243029
    User Muhammadanism id=05L88ACa forwards message
    Current time: 15.1080729341
    User Imogene id=SWhy4mZa forwards message
    Current time: 15.89898774
    User GTE id=wKax992T forwards message
    Current time: 16.6959249629
    
    Average request number: 17
    
    Aggregated data...
    Answer "A Beautiful mind" got 33.0% of votes
    Answer "Terminator" got 33.0% of votes
    Answer "Matrix" got 33.0% of votes


---
**Q&A**
1. Average number of request. How do we calculate it?
 In order to calculate total number of requests we calculate all send/receive events in simulation class. Parameter reponsible for storing this value is called ```_avg_request_number```. To see the values of this parameter after simulation the program has to be called with ```--show-total-statistics``` key.

For example:

    python simulation.py --show-total-statistics

    ...
    Average request number: 27
    
    Aggregated data...
    Answer "A Beautiful mind" got 40.0% of votes
    Answer "Matrix" got 60.0% of votes
2. Show looping prevention.
According to our assumptions we store contacts as a tree structure. By definition this structure can't have cycles, therefore there is no cross-connection between nodes. We have only connections of type parent-child. There're neither parent-parent nor child-child connections. Thus, loops can't appear.
3. Simulate profile?
In order to simulate profile we've written ```ContactsManager``` and ```ContactsTree``` classes. These components are supposed to generate profile and tree of contacts.
```ContactsManager``` generates a random profile by combining name, gender and age (a few words about generation of age will be said next).
```ContactsTree``` class creates a tree structure of contacts tree. At the end we got a root of the contacts tree. We interpret this root as a sender in scope of our simulations.
Example of generated contacts tree is given next.

    {
            "gender": "M", 
            "age": 22, 
            "contacts": [
                {
                    "gender": "M", 
                    "age": 24, 
                    "name": "Actaeon", 
                    "uid": "PjbUk7OM"
                }, 
                {
                    "gender": "F", 
                    "age": 28, 
                    "name": "Carpenter", 
                    "uid": "EgNwV5Fl"
                }, 
                {
                    "gender": "M", 
                    "age": 30, 
                    "name": "Sahara", 
                    "uid": "yIwpScmD"
                }, 
                {
                    "gender": "M", 
                    "age": 25, 
                    "name": "Hezbollah", 
                    "uid": "WLRBEyop"
                }, 
                {
                    "gender": "M", 
                    "age": 26, 
                    "name": "Sandinista", 
                    "uid": "VBOQ8lCY"
                }
            ], 
            "id": "EOjIrHWt", 
            "name": "Sam"
        }
4. Simulate profile spreading (not clear)
5. Simulate QP
6. How do we simulate the age? How to model age clustering (what parameters describe age clustering)?
We've made an assumption that a person has mostly friends of his age range. In other words, the probability to have a friend of 26 years old is higher than probability to have friend of 60 years old, for person who is 24.
Hense, we assume that age ranges of a person's friends are disributed according to Gauss's law.
To simulate age ranges we generate normal distributed random numbers.
Sinse we model age generation as normal destibuted random values we have two major parameters: mean and standart deaviation. More precisely we have the following distribution function $ f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-(x-\mu)^2/2\sigma^2}$. Here $\mu$ - average age of person (mean), $\sigma$ - age standart deviation.
To see age ranges distribution in simulation you need to use
```--show-age-clusterization``` key.

Example:

    python simulation.py --show-age-clusterization

![enter image description here](http://snag.gy/c0ikj.jpg)


1. Oportunistic profile spreading. We agregate all the information in transitional nodes.
2. What parameters influence reply willingness factor?
Reply event in our simulation system is a random event. The probability of this random event has exponential distribution.
The probability density function looks as follows $f(x) = \lambda e^{-\lambda x}$. In our case parameter $\lambda=\frac{1}{age}$.
We interpret such assumptions as follows. Probability of reply grows back proportional to person age.
Next figure show the probability density of exponential distribution.
![enter image description here](http://www.engineeredsoftware.com/nasa/images/expone1.gif)
3. What parameters influence forward willingness factor?
We have the same assumptions and math uder it as it was in section 2.
4. Reply speed. ***Unknown***.
5. Request margin. The total number of replies is up to the user. A user determines how many replies he needs.


Ref: http://pythontips.com/2013/08/08/storing-and-loading-data-with-json/

