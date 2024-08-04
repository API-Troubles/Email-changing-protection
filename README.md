# Email Changing Protection

## How to implement

Most of this project revoloves around the demo to test this. But what is most important is the questions and verification systems. Implement it how you wish.

The following yes/no questions are used. [x] indicates what should be a yes response and [ ] indicates what should be a no response. If any question is answered incorrectly then the email should not be changed and the user warned.

Ensure the user can't be socially engineered into providing responses by adding safeguards.

A good example would be to add pre-text for the user to read.
```
Please Read: Answer these questions by yourself. Don't let anyone else tell you how to answer. If you are unsure or feel pressured, feel free to contact our support team.
```

### Confirmation of email ownership and choice:
- [x] Do you/a family member own [email]?
- [x] Is this your decision to change this email, and NOT anyone else not family?

### Identification of common scams
- [ ] Did tech support tell you to change your email?
- [ ] Did we tell you to change your email?
- [ ] Is changing your email something someones told you needs to be done quickly?
- [ ] Is someone telling you to change your email that is NOT family?
- [ ] Did someone not family tell you to change your email by phone, text or email?

### Final Checks
Why are you changing your email address?

a) Official Email
b) Unsolicited message or call
c) A trusted friend or family member
d) You decided on your own


(The next question is to appear if the user selected a or b from above)

- [x] Are you aware of how scams work?
If the user responds no, they should be redirected to a guide on how scams work.