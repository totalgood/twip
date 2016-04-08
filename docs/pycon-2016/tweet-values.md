# Tweet Values

## How TO: Give A Twitter Bot Morals, Values, Ethics

How would you do it?
How would you do it for a child?
How would you do it for a friend, coworker?

### Problem

- Your bot will likely exhibit your own biases
  - You built it
  - You trained it

### Upvoting (Affirmative Action)

- Upweight the "Likes" by less privileged segments of your audience
  - What about hate-likes?
  - What if you don't have a diverse audience
      - Make friends
      - Follow people you admire that are different from you
      - Mimic underprivleged tweeters with few priviledged class followers
  - What if you are member of some underprivileged class?
      - You still want to serve people from different backgrounds
      - It might be valuable to "cater" to and influence privileged classes

```python
conf.affirmation_boost = 1.5
df[df.segment > 0]['likes'] = df[df.segment > 0]['likes'] * conf.affirmation_boost
```
### Upbringing (Training)

- Sample Bias
  - Find training sets that reflect your values
    - population segments you want to boost
