# Email Phishing/Scam Protection Concept

A few weeks ago, a friend of mine had their account hacked on Discord. The attacker socially engineered them to change their recovery email. They recovered their account since, but I wondered, how could companies prevent this? For such large companies, the best they can do is a bit of "don't share your 2fa code" in the bottom corner of an email. Some don't even include stuff like this anymore.

The goal of this project is to show what companies can do (If only they cared) to improve their services and to prevent the daily scams that cause people to lose millions. If somehow your a company reading this, please, you can prevent scams with things as simple as this (maybe implemented better than me).

## How to implement

Most of this project revolves around the demo to test this. However, the most important issues are the questions and verification systems. Implement it how you wish.

The following yes/no questions are used. [x] indicates what should be a yes response and [ ] indicates what should be a no response. If any question is answered incorrectly then the email should not be changed and the user warned.

Ensure the user can't be socially engineered to respond by adding safeguard messages.

A good example would be to add pre-text for the user to read.
```
Please Read: Answer these questions by yourself. Don't let anyone else tell you how to answer. If you are unsure or feel pressured, feel free to contact our support team.
```

### Confirmation of email ownership and choice:
- [x] Do you/a family member own [email]?
- [x] Is this your decision to change this email, and NOT anyone else not family?
- [ ] Does someone not family have access to your computer? Did they tell you to install software like LogMeIn, TeamViewer or GoToAssist?

### Final Checks
Why are you changing your email address?

 Official email
 I was told by a trusted family member / friend
 I was told by someone NOT trusted family / friend
 Tech support told me to
 I was told to by you
 I decided to myself

- [x] Are you aware of how scams work?
If the user responds no, they should be redirected to a guide on how scams work.

- [ ] Did someone say this is an urgent matter?
