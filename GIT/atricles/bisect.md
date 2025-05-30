No matter how thorough your [test coverage](https://remimercier.com/series/rspec/) is, you can’t test everything.

One day, you’ll introduce a regression in your application, and you won’t notice it straight away. When you finally realize you broke your feature, it can be hard to pinpoint where and when it happened. It’s even harder when several people are working on the same application.

Now is a good time to get acquainted with **`git bisect`**.

Ready to time travel through your application?

## The inefficient way of debugging: checking every commit, one by one

The other day, the situation described above happened to me.

My first instinct was to browse the list of commits and check each one for breaking changes. I kept throwing wild guesses for an hour before giving up.

Antichronologically looking through your commit list is a real-life example of [quadratic](https://jvns.ca/blog/2021/09/10/hashmaps-make-things-fast/) searches.

It might work if you have a couple of commits. But the more commits you need to check, the exponentially[1](https://remimercier.com/how-to-use-git-bisect/#fn:1) longer it’ll take.

On the other hand, `git bisect` uses a binary search algorithm to search through your list of commits. And it’s fast!

Ok, but what is a binary search?

A binary search takes a sorted list of information. Instead of checking elements one by one, from first to last, the algorithm jumps straight to the middle element.

Based on the condition of your search, the algorithm will either:

- return the current element
- inspect the left-hand side of your list
- inspect the right-hand side of your list

At each iteration, the algorithm checks the middle element in an ever-narrowing list.

TL;DR: A binary search doesn’t check every element in the list. Only a fraction of them.

`git bisect` works in a similar way.

## The efficient way of debugging: `git bisect`

Right now, your application doesn’t work as intended. But you _do_ know that two months ago, your application was working fine. Somewhere in your list of commits, you introduced a regression.

The problem? You don’t know when.

There is one commit that draws a line in your application’s timeline:

- before that faulty commit, your application worked fine
- after that faulty commit, your application crashes

`git bisect` leverages binary search to pinpoint the commit that introduced the regression.

It uses the most recent “bad” commit and the last know “good” commits as a range.

`git bisect` picks a commit in the middle of that range and asks you whether the selected commit is “good” or “bad”. It continues narrowing down the range until it finds the exact commit that introduced the change.

Let’s try it:

```
➜  my-app git:(main) ✗ git bisect start
➜  my-app git:(main|BISECTING) ✗ git bisect bad
➜  my-app git:(main|BISECTING) ✗ git bisect good ae998022
Bisecting: 4 revisions left to test after this (roughly 4 steps)
[02ca345f3e29217bb6553] Refactor the asset pipeline
```

Here’s a breakdown:

- `git bisect start` lets you enter the `bisect` mode.
- `git bisect bad`: tells `bisect` that the current HEAD doesn’t work.
- `git bisect good <commit sha>`: tells `bisect` the last known working commit.
- `Bisecting: 4 revisions left...`: an estimated number of steps
- `[02ca345f3e29217bb6553] Refactor...`: the commit your app is currently staged.

Instead of checking commits one by one, `git bisect` jumps to the middle commit in your list (here, the commit `02ca345f3e29217bb6553`) and **stage your application in the state it was at that time**. Fancy!

You can now interact with your application. Run your tests. Go and try the faulty feature in your local environment. I repeat, go and check your app. Click on something!

Why am I insisting on this? Because the first time I used `bisect`, I had a preconception about the commit that had introduced the bug. Instead of testing my application at each stage of the process, I told `git bisect` what I imagined the state was. I ended up in a self-referential loop that led me to the commit I assumed in the first place.

Once I started using `git bisect` correctly, I realized I was quite wrong about the breaking commit.

Back to our current `bisect`.

```
➜  my-app git:(main) ✗ git bisect start
➜  my-app git:(main|BISECTING) ✗ git bisect bad
➜  my-app git:(main|BISECTING) ✗ git bisect good ae998022
Bisecting: 4 revisions left to test after this (roughly 4 steps)
[02ca345f3e29217bb6553] Refactor the asset pipeline

➜  my-app git:((02ca345f3...)|BISECTING) ✗ git bisect bad
Bisecting: 11 revisions left to test after this (roughly 3 steps)
[76c502e15dba8ac5b] Add new feature
```

Your application is currently running in the `02ca345f3e29217bb6553` commit’s state.

If this current state is faulty, it means the bug was introduced earlier. When typing `git bisect bad`, `git bisect` takes a note about the non-working state of your application then jumps to the middle commit on the left-hand side of our range (i.e. older commits).

![[bisect_images/0885ea6033d478e2503e4be04112c298_MD5.jpg]]

If the application works fine in the current state, `git bisect good` will prompt `git bisect` to explore the right-hand side of our range (i.e. newer commits).

![[bisect_images/cc09619618f141728919f32c467c017c_MD5.jpg]]

Repeat until there are no revisions left.

```
➜  my-app git:(main) ✗ git bisect start
➜  my-app git:(main|BISECTING) ✗ git bisect bad
➜  my-app git:(main|BISECTING) ✗ git bisect good ae998022
Bisecting: 4 revisions left to test after this (roughly 4 steps)
[02ca345f3e29217bb6553] Refactor the asset pipeline

➜  my-app git:((02ca345f3...)|BISECTING) ✗ git bisect bad
Bisecting: 11 revisions left to test after this (roughly 3 steps)
[76c502e15dba8ac5b] Add new feature

➜  my-app git:((76c502e15...)|BISECTING) ✗ git bisect bad
Bisecting: 3 revisions left to test after this (roughly 2 steps)
[e7e6f2ab20a7f9b] Merge branch 'new-payment-system' into 'main'

➜  my-app git:((e7e6f2ab2...)|BISECTING) ✗ git bisect bad
Bisecting: 1 revision left to test after this (roughly 1 step)
[4a6d8943db4e2d] Change CORS

➜  my-app git:((4a6d8943d...)|BISECTING) ✗ git bisect bad
Bisecting: 0 revisions left to test after this (roughly 1 step)
[996e5a376c7b9] Update GEMFILE

➜  my-app git:((a7c40a681...)|BISECTING) ✗ git bisect bad
a7c40a6818c34f1ea1 is the first bad commit
commit a7c40a6818c34f1ea1
Merge: xxx xxx
Author: Remi Mercier
Date:   Tue Aug 3 13:51:20 2021 +0000
```

An aside: if you need to try your app in real life, it probably means you need to write a test of some kind. In my case, the problem would have required an integration test and mocking responses between two services.

It’s just so much faster than looking for things in the dark!

If you can’t try the commit `git bisect` currently outputs, you can use `git bisect skip` and, `git bisect` will move on to the next commit.

Feeling adventurous? You can check the official documentation for [git bisect](https://git-scm.com/docs/git-bisect).


