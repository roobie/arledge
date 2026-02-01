Martin Blais, December 2016

[http://furius.ca/beancount/doc/double-entry](http://furius.ca/beancount/doc/double-entry)

[Introduction](https://beancount.github.io/docs/the_double_entry_counting_method.html#introduction)

[Basics of Double-Entry Bookkeeping](https://beancount.github.io/docs/the_double_entry_counting_method.html#basics-of-double-entry-bookkeeping)

> [Statements](https://beancount.github.io/docs/the_double_entry_counting_method.html#statements)
> 
> [Single-Entry Bookkeeping](https://beancount.github.io/docs/the_double_entry_counting_method.html#single-entry-bookkeeping)
> 
> [Double-Entry Bookkeeping](https://beancount.github.io/docs/the_double_entry_counting_method.html#double-entry-bookkeeping)
> 
> [Many Accounts](https://beancount.github.io/docs/the_double_entry_counting_method.html#many-accounts)
> 
> [Multiple Postings](https://beancount.github.io/docs/the_double_entry_counting_method.html#multiple-postings)

[Types of Accounts](https://beancount.github.io/docs/the_double_entry_counting_method.html#types-of-accounts)

[Trial Balance](https://beancount.github.io/docs/the_double_entry_counting_method.html#trial-balance)

[Income Statement](https://beancount.github.io/docs/the_double_entry_counting_method.html#income-statement)

[Clearing Income](https://beancount.github.io/docs/the_double_entry_counting_method.html#clearing-income)

[Equity](https://beancount.github.io/docs/the_double_entry_counting_method.html#equity)

[Balance Sheet](https://beancount.github.io/docs/the_double_entry_counting_method.html#balance-sheet)

[Summarizing](https://beancount.github.io/docs/the_double_entry_counting_method.html#summarizing)

[Period Reporting](https://beancount.github.io/docs/the_double_entry_counting_method.html#period-reporting)

[Chart of Accounts](https://beancount.github.io/docs/the_double_entry_counting_method.html#chart-of-accounts)

> [Country-Institution Convention](https://beancount.github.io/docs/the_double_entry_counting_method.html#country-institution-convention)

[Credits & Debits](https://beancount.github.io/docs/the_double_entry_counting_method.html#credits-debits)

[Accounting Equations](https://beancount.github.io/docs/the_double_entry_counting_method.html#accounting-equations)

[Plain-Text Accounting](https://beancount.github.io/docs/the_double_entry_counting_method.html#plain-text-accounting)

[The Table Perspective](https://beancount.github.io/docs/the_double_entry_counting_method.html#the-table-perspective)

## Introduction[](https://beancount.github.io/docs/the_double_entry_counting_method.html#introduction "Permanent link")

This document is a gentle introduction to the double-entry counting method, as written from the perspective of a computer scientist. It is an attempt to explain basic bookkeeping using as simple an approach as possible, doing away with some of the idiosyncrasies normally involved in accounting. It is also representative of how [Beancount](http://furius.ca/beancount/) works, and it should be useful to all users of [plain-text accounting](http://plaintextaccounting.org/).

Note that I am not an accountant, and in the process of writing this document I may have used terminology that is slightly different or unusual to that which is taught in perhaps more traditional training in accounting. I granted myself license to create something new and perhaps even unusual in order to explain those ideas as simply and clearly as possible to someone unfamiliar with them.

I believe that the method of double-entry counting should be taught to everyone at the high school level everywhere as it is a tremendously useful organizational skill, and I hope that this text can help spread its knowledge beyond professional circles.

## Basics of Double-Entry Bookkeeping[](https://beancount.github.io/docs/the_double_entry_counting_method.html#basics-of-double-entry-bookkeeping "Permanent link")

The double-entry system is just a simple _method of counting_, with some simple rules.

Let’s begin by defining the notion of an **account**. An account is something that can contain things, like a bag. It is used to count things, to accumulate things. Let’s draw a horizontal arrow to visually represent the evolving contents of an account over time:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/2f37aa3938d599d4783ca9b74965026fba0a3b50.png)

On the left, we have the past, and to the right, increasing time: the present, the future, etc.

For now, let’s assume that accounts can contain only one kind of thing, for example, _dollars_. All accounts begin with an empty content of zero dollars. We will call the number of units in the account the **balance** of an account. Note that it represents its contents at a particular point in time. I will draw the balance using a number above the account’s timeline:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/54633827be99c315dc937778221752b848411ca9.png)

The contents of accounts can change over time. In order to change the content of an account, we have to add something to it. We will call this addition a **posting** to an account, and I will draw this change as a circled number on the account’s timeline, for example, adding $100 to the account:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/004bc3354eb84bf554a8e5080a21f8d16fc29d82.png)

Now, we can draw the updated balance of the account after the posting with another little number right after it:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/6281f96c3465982c6bf48fccb302b40f90890311.png)

The account’s balance, after adding $100, is now $100.

We can also remove from the contents of an account. For example, we could remove $25, and the resulting account balance is now $75:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/1672e121ec80f8fcdb158bb497e05e6dc809dee5.png)

Account balances can also become _negative_, if we remove more dollars than there are in the account. For example, if we remove $200 from this account, the balance now becomes $-125:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/862c0b57a35631a52eead2cf8cdd7b5f2a1aa106.png)

It’s perfectly fine for accounts to contain a negative balance number. Remember that all we’re doing is counting things. As we will see shortly, some accounts will remain with a negative balance for most of their timeline.

### Statements[](https://beancount.github.io/docs/the_double_entry_counting_method.html#statements "Permanent link")

Something worthy of notice is how the timeline notation I’ve written in the previous section is analogous to paper account statements institutions maintain for each client and which you typically receive through the mail:

| _**Date**_ | _**Description**_ | _**Amount**_ | _**Balance**_ |
| --- | --- | --- | --- |
| 2016-10-02 | ... | 100.00 | 1100.00 |
| 2016-10-05 | ... | \-25.00 | 1075.00 |
| 2016-10-06 | ... | \-200.00 | 875.00 |
| _**Final Balance**_ | 875.00 |  |  |

Sometimes the amount column is split into two, one showing the positive amounts and the other the negative ones:

| _**Date**_ | _**Description**_ | _**Debit**_ | _**Credit**_ | _**Balance**_ |
| --- | --- | --- | --- | --- |
| 2016-10-02 | ... |  | 100.00 | 1100.00 |
| 2016-10-05 | ... | 25.00 |  | 1075.00 |
| 2016-10-06 | ... | 200.00 |  | 875.00 |
| _**Final Balance**_ | 875.00 |  |  |  |

Here, “debit” means “removed from your account” and “credit” means “deposited in your account.” Sometimes the words “withdrawals” and “deposits” will be used. It all depends on context: for checking and savings accounts it is usual to have both types of postings, but for a credit card account typically it shows only positive numbers and then the occasional monthly payment so the single column format is used.

In any case, the “balance” column always shows the resulting balance _after_ the amount has been posted to the account. And sometimes the statements are rendered in decreasing order of time.

### Single-Entry Bookkeeping[](https://beancount.github.io/docs/the_double_entry_counting_method.html#single-entry-bookkeeping "Permanent link")

In this story, this account belongs to someone. We’ll call this person the **owner** of the account. The account can be used to represent a real world account, for example, imagine that we use it to represent the content of the owner’s checking account at a bank. So we’re going to label the account by giving it a name, in this case “Checking”:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/a4ac6f0f3d2cf7df150fd501f0ab9a5942f79a80.png)

Imagine that at some point, this account has a balance of $1000, like I’ve drawn on the picture. Now, if the owner spends $79 of this account, we would represent it like this:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/75337406afb5f23c23733fd25be8683ae151b410.png)

Furthermore, if the expense was for a meal at a restaurant, we could flag the posting with a **category** to indicate what the change was used for. Let’s say, “Restaurant”, like this:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/d7f6ec08cb13d409752000bb42495399abc85848.png)

Now, if we have a lot of these, we could write a computer program to accumulate all the changes for each category and calculate the sums for each of them. That would tell us how much we spent in restaurants in total, for example. This is called the **single-entry method** of accounting.

But we’re not going to do it this way; we have a better way. Bear with me for a few more sections.

### Double-Entry Bookkeeping[](https://beancount.github.io/docs/the_double_entry_counting_method.html#double-entry-bookkeeping "Permanent link")

An owner may have multiple accounts. I will represent this by drawing many similar account timelines on the same graphic. As before, these are labeled with unique names. Let’s assume that the owner has the same “Checking” account as previously, but now also a **“**Restaurant**”** account as well, which can be used to accumulate all food expenses at restaurants. It looks like this:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/3088280515ab5b6da599edd5a1b2ca30100f2b0b.png)

Now, instead of _categorizing_ the posting to a “restaurant category” as we did previously, we could create a matching posting on the “Restaurant” account to record how much we spent for food, with the amount spent ($79):

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/2801d8aff3ccd91dcd584f58a5bcabbb57fb19d4.png)

The “Restaurant” account, like all other accounts, also has an accumulated balance, so we can find out how much we spent in “Restaurant” in total. This is entirely symmetrical to counting changes in a checking account.

Now, we can associate the two postings together, by creating a kind of “parent” box that refers to both of them. We will call this object a **transaction**:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/18524adffedac5e812eb65dcbb179b66b0ae9e53.png)

Notice here that we’ve also associated a description to this transaction: “Dinner at Uncle Boons”. A transaction also has a **date**, and all of its postings are recorded to occur on that date. We call this the transaction date.

We can now introduce the fundamental rule of double-entry bookkeeping system:

```
The sum of all the postings of a transaction must equal zero.
```

Remember this, as this is the foundation of the double-entry method, and its most important characteristic. It has important consequences which I will discuss later in this document.

In our example, we remove $79 from the “Checking” account and “give it” to the “Restaurant” account. ($79) + ($-79) = $0. To emphasize this, I could draw a little summation line under the postings of the transaction, like this:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/a56ad72219b0d8a6c90c692655d1b24459add2d6.png)

### Many Accounts[](https://beancount.github.io/docs/the_double_entry_counting_method.html#many-accounts "Permanent link")

There may be many such transactions, over many different accounts. For example, if the owner of the accounts had a lunch the next day which she paid using a credit card, it could be represented by creating a “Credit Card” account dedicated to tracking the real world credit card balance, and with a corresponding transaction:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/458909db06c7f38f7896205f67d60397b292e7d9.png)

In this example, the owner spent $35 at a restaurant called “Eataly.” The previous balance of the owner’s credit card was $-450; after the expense, the new balance is $-485.

For each real world account, the owner can create a bookkeeping account like we did. Also, for each category of expenditure, the owner also creates a bookkeeping account. In this system, there are no limits to how many accounts can be created.

Note that the balance in the example is a negative number; this is not an error. Balances for credit card accounts are normally negative: they represent an amount _you owe_, that the bank is lending you _on credit_. When your credit card company keeps track of your expenses, they write out your statement from their perspective, as positive numbers. For you, those are amounts you need to eventually pay. But here, in our accounting system, we’re representing numbers from the owner’s point-of-view, and from her perspective, this is money she owes, not something she has. What we have is a meal sitting in our stomach (a positive number of $ of “Restaurant”).

### Multiple Postings[](https://beancount.github.io/docs/the_double_entry_counting_method.html#multiple-postings "Permanent link")

Finally, transactions may have more than two postings; in fact, they may have any number of postings. The only thing that matters is that the sum of their amounts is zero (from the rule of double-entry bookkeeping above).

For example, let’s look at what would happen if the owner gets her salary paid for December:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/19e2cc49a057dfeea1cf5254610eab4c9a124488.png)

Her gross salary received in this example is recorded as $-2,905 (I’ll explain the sign in a moment). $905 is set aside for taxes. Her “net” salary of $2,000, the remainder, is deposited in her “Checking” account and the resulting balance of that account is $2,921 (the previous balance of $921 + $2,000 = $2,921). This transaction has three postings: (+2,000) + (-2,905) + (+905) = 0. The double-entry rule is respected.

Now, you may ask: Why is her salary recorded as a negative number? The reasoning here is similar to that of the credit card above, though perhaps a bit more subtle. These accounts exist to track all the amounts from the owner’s point-of-view. The owner gives out work, and receives money and taxes in exchange for it (positive amounts). The work given away is denominated in dollar units. It “leaves” the owner (imagine that the owner has _potential work_ stored in her pocket and as she goes into work every day sprinkles that work potential giving it to the company). The owner _gave_ $2,905’s worth of work away. We want to track how much work was given, and it’s done with the “Salary” account. That’s her gross salary.

Note also that we’ve simplified this paycheck transaction a bit, for the sake of keeping things simple. A more realistic recording of one’s pay stub would have many more accounts; we would separately account for state and federal tax amounts, as well as social security and medicare payments, deductions, insurance paid through work, and vacation time accrued during the period. But it wouldn’t be much more complicated: the owner would simply translate all the amounts available from her pay stub into a single transaction with more postings. The structure remains similar.

## Types of Accounts[](https://beancount.github.io/docs/the_double_entry_counting_method.html#types-of-accounts "Permanent link")

Let’s now turn our attention to the different types of accounts an owner can have.

**Balance or Delta.** First, the most important distinction between accounts is about whether we care about the balance **at a particular point** in time, or whether it only makes sense to care about differences **over a period** of time. For example, the balance of someone’s Checking or Savings accounts is a meaningful number that both the owner and its corresponding bank will care about. Similarly, the total amount owed on someone’s Credit Card account is also meaningful. The same goes with someone’s remaining Mortgage amount to pay on a house.

On the other hand, the total amount of Restaurant expenses since the beginning of somebody’s life on earth is not particularly interesting. What we might care about for this account is the amount of Restaurant expenses incurred _over a particular period of time_. For example, “how much did you spend in restaurants last month?” Or last quarter. Or last year. Similarly, the total amount of gross salary since the beginning of someone’s employment at a company a few years ago is not very important. But we would care about the total amount earned during a tax year, that is, for that time period, because it is used for reporting one’s income to the tax man.

-   Accounts whose balance at a point in time is meaningful are called **balance sheet accounts**. There are two types of such accounts: “**Assets**” and “**Liabilities**.”
    
-   The other accounts, that is, those whose balance is not particularly meaningful but for which we are interested in calculating changes over a period of time are called **income statement accounts**. Again, there are two kinds: “**Income**” and “**Expenses**.”
    

**Normal sign.** Secondly, we consider _the usual sign of an account’s balance_. The great majority of accounts in the double-entry system tend to have a balance with always a positive sign, or always a negative sign (though as we’ve seen previously, it is not impossible that an account’s balance could change signs). This is how we will distinguish between the pairs of accounts mentioned before:

-   For a balance sheet account, Assets normally have positive balances, and Liabilities normally have negative balances.
    
-   For income statement accounts, Expenses normally have a positive balance, and Income accounts normally have a negative balance.
    

This situation is summarized in the following table:

|  | Balance: Positive (+) | Balance: Negative (-) |
| --- | --- | --- |
| 
Balance matters  
**at a point** in time

(Balance Sheet)

 | **Assets** | **Liabilities** |
| 

**Change** in balance matters  
**over a period** of time

(Income Statement)

 | **Expenses** | **Income** |

Let’s discuss each type of account and provide some examples, so that it doesn’t remain too abstract.

-   **Assets. (+)** Asset accounts represent _something the owner has_. A canonical example is banking accounts. Another one is a “cash” account, which counts how much money is in your wallet. Investments are also assets (their units aren’t dollars in this case, but rather some number of shares of some mutual fund or stock). Finally, if you own a home, the home itself is considered an asset (and its market value fluctuates over time).
    
-   **Liabilities.** **(-)** A liability account represents _something the owner owes_. The most common example is a credit card. Again, the statement provided by your bank will show positive numbers, but from your own perspective, they are negative numbers. A loan is also a liability account. For example, if you take out a mortgage on a home, this is money you owe, and will be tracked by an account with a negative amount. As you pay off the mortgage every month the negative number goes up, that is, its absolute value gets smaller and smaller over time (e.g., -120,000 -> -117,345).
    
-   **Expenses. (+)** An expense account represents _something you’ve received_, perhaps by exchanging something else to purchase it. This type of account will seem pretty natural: food, drinks, clothing, rent, flights, hotels and most other categories of things you typically spend your disposable income on. However, taxes are also typically tracked by an expense account: when you receive some salary income, the amount of taxes withheld at the source is recorded immediately as an expense. Think of it as paying for government services you receive throughout the year.
    
-   **Income.** **(-)** An income account is used to count _something you’ve given away_ in order to receive something else (typically assets or expenses). For most people with jobs, that is the value of their time (a salary income). Specifically, here we’re talking about the _gross_ income. For example, if you’re earning a salary of $120,000/year, that number is $120,000, not whatever amount remains after paying for taxes. Other types of income includes dividends received from investments, or interest paid from bonds held. There are also a number of oddball things received you might record as income, such the value of rewards received, e.g., cash back from a credit card, or monetary gifts from someone.
    

In Beancount, all account names, without exception, must be associated to one of the types of accounts described previously. Since the type of an account never changes during its lifetime, we will make its type a part of an account’s name, as a _prefix_, by convention. For example, the qualified account name for restaurant will be “Expenses:Restaurant”. For the bank checking account, the qualified account name will be “Assets:Checking”.

Other than that, you can select any name you like for your accounts. You can create as many accounts as you like, and as we will see later, you can organize them in a hierarchy. As of the writing of this document, I’m using more than 700 accounts to track my personal affairs.

Let us now revisit our example and add some more accounts:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/281c7a6ed22a8168fc1094a1faa61f2b0fdd7ca3.png)

And let’s imagine there are more transactions:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/e3008a34f9ce7a224e33d4cbb79bcebbb08d418e.png)

… and even more of them:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/18b769f7a3cdf7fd67a983d3a39325b563d8d346.png)

Finally, we can label each of those accounts with one of the four types of accounts by prepending the type to their account names:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/1f84bcb0ad4787659c157280f6f4ae5ea720482d.png)

A realistic book from someone tracking all of their personal affairs might easily contain thousands of transactions per year. But the principles remain simple and they remain the same: postings are applied to accounts over time, and must be parented to a transaction, and within this transaction the sum of all the postings is zero.

When you do **bookkeeping** for a set of accounts, you are essentially describing all the postings that happen on all the accounts over time, subject to the constraint of the rule. You are creating a database of those postings in a **book**. You are “keeping the book,” that is, traditionally, the book which contains all those transactions. Some people call this “maintaining a journal.”

We will now turn our attention to obtaining useful information from this data, summarizing information from the book.

## Trial Balance[](https://beancount.github.io/docs/the_double_entry_counting_method.html#trial-balance "Permanent link")

Take our last example: we can easily reorder all the accounts such that all the Asset accounts appear together at the top, then all the Liabilities accounts, then Income, and finally Expenses accounts. We are simply changing the order without modifying the structure of transactions, in order to group each type of accounts together:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/175f3223735d9d04b2a7e3f421bc6280f3cda5eb.png)

We’ve reordered the accounts with Assets accounts grouped at the top, then Liabilities, then some Equity accounts (which we have just introduced, more about them is discussed later), then Income and finally Expenses at the bottom.

If we sum up the postings on all of the accounts and render just the account name and its final balance on the right, we obtain a report we call the “trial balance.”

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/71edc0da7e156b4e07cd6f4f0addded7f15cb33e.png)

This simply reflects the balance of each account at a particular point in time. And because each of the accounts began with a zero balance, and each transaction has itself a zero balance, we know that the sum of all those balances must equal zero.<sup id="fnref:1"><a href="https://beancount.github.io/docs/the_double_entry_counting_method.html#fn:1">1</a></sup> This is a consequence of our constraining that each of the postings be part of a transaction, and that each transaction have postings that balance each other out.

## Income Statement[](https://beancount.github.io/docs/the_double_entry_counting_method.html#income-statement "Permanent link")

One kind of common information that is useful to extract from the list of transactions is a summary of changes in income statement accounts during a particular period of time. This tells us how much money was earned and spent during this period, and the difference tells us how much profit (or loss) was incurred. We call this the “net income.”

In order to generate this summary, we simply turn our attention to the balances of the accounts of types Income and Expenses, summing up just the transactions for a particular period, and we draw the Income balances on the left, and Expenses balances on the right:

![out.png](https://beancount.github.io/docs/the_double_entry_counting_method/media/6d57026ecb4c28873f77167eb49ea8025bbf150b.png)

It is important to take note of the signs here: Income numbers are negative, and Expenses numbers are positive. So if you earned more than you spent (a good outcome), the final sum of Income + Expenses balances will be a negative number. Like any other income, a net income that has a negative number means that there is a corresponding amount of Assets and/or Liabilities with positive numbers (this is good for you).

An Income Statement tells us what changed during a particular period of time. Companies typically report this information **quarterly** to investors and perhaps the public (if they are a publicly traded company) in order to share how much profit they were able to make. Individuals typically report this information on their **annual** tax returns.

## Clearing Income[](https://beancount.github.io/docs/the_double_entry_counting_method.html#clearing-income "Permanent link")

Notice how in the income statement only the transactions within a particular interval of time are summed up. This allows one, for instance, to compute the sum of all income earned during a year. If we were to sum up all of the transactions of this account since its inception we would obtain the total amount of income earned since the account was created.

A better way to achieve the same thing is to zero out the balances of the Income and Expenses accounts. Beancount calls this basic transformation “clearing<sup id="fnref:2"><a href="https://beancount.github.io/docs/the_double_entry_counting_method.html#fn:2">2</a></sup>.” It is carried out by:

1.  Computing the balances of those accounts from the beginning of time to the start of the reporting period. For example, if you created your accounts in year 2000 and you wanted to generate an income statement for year 2016, you would sum up the balances from 2000 to Jan 1, 2016.
    
2.  Inserting transactions to empty those balances and transfer them to some other account that isn’t Income nor Expenses. For instance, if the restaurant expense account for those 16 years amounts to $85,321 on Jan 1, 2016, it would insert a transaction of $-85,321 to restaurants and $+85,321 to “previous earnings”. The transactions would be dated Jan 1, 2016. Including this transaction, the sum of that account would zero on that date. This is what we want.
    

Those transactions inserted for all income statement accounts are pictured in green below. Now summing the entire set of transactions through the end of the ledger would yield only the changes during year 2016 because the balances were zero on that date:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/7f10adb5a661d0aa0b66f5f66aafb3ff5eefa212.png)

This is the semantics of the “CLEAR” operation of the bean-query shell.

(Note that another way to achieve the same thing for income statement accounts would be to segregate and count amounts only for the transactions after the clearing date; however, jointly reporting on income statement accounts and balance sheet accounts would have incorrect balances for the balance sheet accounts.)

## Equity[](https://beancount.github.io/docs/the_double_entry_counting_method.html#equity "Permanent link")

The account that receives those previously accumulated incomes is called “Previous Earnings”. It lives in a fifth and final type of accounts: **Equity**. We did not talk about this type of accounts earlier because they are most often only used to transfer amounts to build up reports, and the owner usually doesn’t post changes to those types of accounts; the software does that automatically, e.g., when clearing net income.

The account type “equity” is used for accounts that hold a summary of the net income implied by all the past activity. The point is that if we now list together the Assets, Liabilities and Equity accounts, because the Income and Expenses accounts have been zero’ed out, the sum total of all these balances should equal exactly zero. And summing up all the Equity accounts clearly tells us what’s our stake in the entity, in other words, if you used the assets to pay off all the liabilities, how much is left in the business… how much it’s worth.

Note that the normal sign of the Equity accounts is _negative_. There is no particular meaning to that, just that they are used to counterbalance Assets and Liabilities and if the owner has any value, that number should be negative. (A negative Equity means some positive net worth.)

There are a few different Equity accounts in use in Beancount:

-   **Previous Earnings** or **Retained Earnings.** An account used to hold the sum total of Income & Expenses balances from the beginning of time until the _beginning_ of a reporting period. This is the account we were referring to in the previous section.
    
-   **Current Earnings**, also called **Net Income.** An account used to contain the sum of Income & Expenses balances incurred _during_ the reporting period. They are filled in by “clearing” the Income & Expenses accounts _at the end_ of the reporting period.
    
-   **Opening Balances.** An equity account used to counterbalance deposits used to initialize accounts. This type of account is used when we truncate the past history of transactions, but we also need to ensure that an account’s balance begins its history with a particular amount.
    

Once again: you don’t need to define nor use these accounts yourself, as these are created for the purpose of summarizing transactions. Generally, the accounts are filled in by the clearing process described above, or filled in by Pad directives to “opening balances” equity accounts, to account for summarized balances from the past. They are created and filled in automatically by the software. We’ll see how these get used in the following sections.

## Balance Sheet[](https://beancount.github.io/docs/the_double_entry_counting_method.html#balance-sheet "Permanent link")

Another kind of summary is a listing of the owner’s assets and debts, for each of the accounts. This answers the question: “_Where’s the money?_” In theory, we could just restrict our focus to the Assets and Liabilities accounts and draw those up in a report:

![out.png](https://beancount.github.io/docs/the_double_entry_counting_method/media/093cd8751f07c38e909b7621675daa80db8fb634.png)

However, in practice, there is another closely related question that comes up and which is usually answered at the same time: “_Once all debts are paid off, how much are we left with?_” This is called the **net worth**.

If the Income & Expenses accounts have been cleared to zero and all their balances have been transferred to Equity accounts, the net worth should be equal to the sum of all the Equity accounts. So in building up the Balance Sheet, it it customary to clear the net income and then display the balances of the Equity accounts. The report looks like this:

![out.png](https://beancount.github.io/docs/the_double_entry_counting_method/media/d495b61bc719ab90cdfc9fd379ef62531cff0627.png)

Note that the balance sheet can be drawn for _any point in time_, simply by truncating the list of transactions following a particular date. A balance sheet displays a snapshot of balances at one date; an income statement displays the difference of those balances between two dates.

## Summarizing[](https://beancount.github.io/docs/the_double_entry_counting_method.html#summarizing "Permanent link")

It is useful to summarize a history of past transactions into a single equivalent deposit. For example, if we’re interested in transactions for year 2016 for an account which has a balance of $450 on Jan 1, 2016, we can delete all the previous transactions and replace them with a single one that deposits $450 on Dec 31, 2015 and that takes it from somewhere else.

That somewhere else will be the Equity account **Opening Balances**. First, we can do this for all Assets and Liabilities accounts (see transactions in blue):

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/035eb15afa1439450886d6ce20c60013227283b7.png)

Then we delete all the transactions that precede the opening date, to obtain a truncated list of transactions:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/2596047a5cbd9da8a925c7a7ee10fef9681ce472.png)

This is a useful operation when we’re focused on the transactions for a particular interval of time.

(This is a bit of an implementation detail: these operations are related to how Beancount is designed. Instead of making all the reporting operations with parameters, all of its reporting routines are simplified and instead operate on the entire stream of transactions; in this way, we convert the list of transactions to include only the data we want to report on. In this case, summarization is just a transformation which accepts the full set of transactions and returns an equivalent truncated stream. Then, from this stream, a journal can be produced that excludes the transactions from the past.

From a program design perspective, this is appealing because the only state of the program is a stream of transactions, and it is never modified directly. It’s simple and robust.)

## Period Reporting[](https://beancount.github.io/docs/the_double_entry_counting_method.html#period-reporting "Permanent link")

Now we know we can produce a statement of changes over a period of time, by “clearing” and looking at just the Income & Expenses accounts (the Income Statement). We also know we can clear to produce a snapshot of Assets, Liabilities & Equity at any point in time (the Balance Sheet).

More generally, we’re interested in inspecting a particular period of time. That implies an income statement, but also _two_ balance sheet statements: the balance sheet _at the beginning_ of the period, and the balance sheet _at the end_ of the period.

In order to do this, we apply the following transformations:

-   **Open.** We first clear net income at the beginning of the period, to move all previous income balances to the Equity **Previous Earnings** account. We then summarize up to the beginning of the period. We call the combination of clearing + summarizing: “Opening.”
    
-   **Close.** We also truncate all the transactions following the end of the reporting period. We call this operation “Closing.”
    

These are the meaning of the “OPEN” and “CLOSE” operations of the bean-query shell<sup id="fnref:3"><a href="https://beancount.github.io/docs/the_double_entry_counting_method.html#fn:3">3</a></sup>. The resulting set of transactions should look like this.

“Closing” involves two steps. First, we remove all transactions following the closing date:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/e9bbbbdf2a94fe681fd547cf470c4d19ae1e6c0e.png)

We can process this stream of transactions to produce an Income Statement for the period.

Then we clear again at the _end_ date of the desired report, but this time we clear the net income to “Equity:Earnings:Current”:

![](https://beancount.github.io/docs/the_double_entry_counting_method/media/1dc844e93000faa184bd3e1ec3e0cd4e1a9fb5fb.png)

From these transactions, we produce the Balance Sheet at the end of the period.

This sums up the operations involved in preparing the streams of transactions to produce reports with Beancount, as well as a basic introduction to those types of reports.

## Chart of Accounts[](https://beancount.github.io/docs/the_double_entry_counting_method.html#chart-of-accounts "Permanent link")

New users are often wondering how much detail they should use in their account names. For example, should one include the payee in the account name itself, such as in these examples?

```
Expenses:Phone:Mobile:VerizonWireless
Assets:AccountsReceivable:Clients:AcmeInc
```

Or should one use simpler names like the following, relying instead on the “payee”, “tags”, or perhaps some other metadata in order to group the postings?

```
Expenses:Phone
Assets:AccountsReceivable
```

The answer is that _it depends on you_. This is an arbitrary choice to make. It’s a matter of taste. Personally I like to abuse the account names a bit and create long descriptive ones, other people prefer to keep them simple and use tags to group their postings. Sometimes one doesn’t even need to filter subgroups of postings. There’s no right answer, it depends on what you’d like to do.

One consideration to keep in mind is that account names implicitly define a hierarchy. The “:” separator is interpreted by some reporting code to create an in-memory tree and can allow you to collapse a node’s children subaccounts and compute aggregates on the parent. Think of this as an additional way to group postings.

### Country-Institution Convention[](https://beancount.github.io/docs/the_double_entry_counting_method.html#country-institution-convention "Permanent link")

One convention I’ve come up with that works well for my assets, liabilities and income accounts is to root the tree with a code for the country the account lives in, followed by a short string for the institution it corresponds to. Underneath that, a unique name for the particular account in that institution. Like this:

```
<type> : <country> : <institution> : <account>
```

For example, a checking account could be chosen to be “`Assets:US:BofA:Checking`”, where “BofA” stands for “Bank of America.” A credit card account could include the name of the particular type of card as the account name, like “`Liabilities:US:Amex:Platinum`”, which can be useful if you have multiple cards.

I’ve found it doesn’t make sense for me to use this scheme for expense accounts, since those tend to represent generic categories. For those, it seems to make more sense to group them by category, as in using “`Expenses:Food:Restaurant`” instead of just “`Expenses:Restaurant`”.

In any case, Beancount doesn’t enforce anything other than the root accounts; this is just a suggestion and this convention is not coded anywhere in the software. You have great freedom to experiment, and you can easily change all the names later by processing the text file. See the [Cookbook](https://beancount.github.io/docs/command_line_accounting_cookbook.html) for more practical guidance.

## Credits & Debits[](https://beancount.github.io/docs/the_double_entry_counting_method.html#credits-debits "Permanent link")

At this point, we haven’t discussed the concepts of “credits” and “debits.” This is on purpose: Beancount largely does away with these concepts because it makes everything else simpler. I believe that it is simpler to just learn that the signs of Income, Liabilities and Equity accounts are normally negative and to treat all accounts the same way than to deal with the debits and credits terminology and to treat different account categories differently. In any case, this section explains what these are.

As I have pointed out in previous sections, we consider “Income”, “Liabilities” and “Equity” accounts to normally have a negative balance. This may sound odd; after all, nobody thinks of their gross salary as a negative amount, and certainly your credit-card bill or mortgage loan statements report positive numbers. This is because in our double-entry accounting system we consider all accounts to be held _from the perspective of the owner of the account_. We use signs consistent from this perspective, because it makes all operations on account contents straightforward: they’re all just simple additions and all the accounts are treated the same.

In contrast, accountants traditionally keep all the balances of their accounts as positive numbers and then handle postings to those accounts differently depending on the account type upon which they are applied. The sign to apply to each account is entirely dictated by its type: Assets and Expenses accounts are debit accounts and Liabilities, Equity and Income accounts are credit accounts and require a sign adjustment. Moreover, posting a positive amount on an account is called “debiting” and removing from an account is called “crediting.” See [this external document](http://www.accountingtools.com/debits-and-credits), for example, which nearly makes my head explode, and [this recent thread](https://groups.google.com/d/msgid/beancount/CAPD_o%2B8W2BpTA9qtmMvaTdqdW51v%2Bt5uFrMRbZ93aPqoWokzQw%40mail.gmail.com) has more detail. This way of handling postings makes everything much more complicated than it needs to be.

The problem with this approach is that summing of amounts over the postings of a transaction is not a straightforward sum anymore. For example, let’s say you’re creating a new transaction with postings to two Asset accounts, an Expenses account and an Income account and the system tells you there is a $9.95 imbalance error somewhere. You’re staring at the entry intently; which of the postings is too small? Or is one of the postings too large? Also, maybe a new posting needs to be added, but is it to a debit account or to a credit account? The mental gymnastics required to do this are taxing. Some double-entry accounting software tries to deal with this by creating separate columns for debits and credits and allowing the user enter an amount only in the column that corresponds to each posting account’s type. This helps visually, but why not just use signs instead?

Moreover, when you look at the accounting equations, you have to consider their signs as well. This makes it awkward to do transformations on them and make what is essentially a simple summation over postings into a convoluted mess that is difficult to understand.

In plain-text accounting, we would rather just do away with this inconvenient baggage. We just use additions everywhere and learn to keep in mind that Liabilities, Equity and Income accounts normally have a negative balance. While this is unconventional, it’s much easier to grok. And If there is a need to view a conventional report with positive numbers only, we will be able to trigger that in reporting code<sup id="fnref:4"><a href="https://beancount.github.io/docs/the_double_entry_counting_method.html#fn:4">4</a></sup>, inverting the signs just to render them in the output.

Save yourself some pain: Flush your brain from the "debit" and "credit" terminology.

## Accounting Equations[](https://beancount.github.io/docs/the_double_entry_counting_method.html#accounting-equations "Permanent link")

In light of the previous sections, we can easily express the accounting equations in signed terms. If,

-   A = the sum of all Assets postings
    
-   L = the sum of all Liabilities postings
    
-   X = the sum of all Expenses postings
    
-   I = the sum of all Income postings
    
-   E = the sum of all Equity postings
    

We can say that:

```
A + L + E + X + I = 0
```

This follows from the fact that

```
sum(all postings) = 0
```

Which follows from the fact that each transaction is guaranteed to sum up to zero (which is enforced by Beancount):

```
for all transactions t, sum(postings of t) = 0
```

Moreover, the sum of postings from Income and Expenses is the Net Income (NI):

```
NI = X + I
```

If we adjust the equity to reflect the total Net Income effect by clearing the income to the Equity retained earnings account, we get an updated Equity value (E’):

```
E’ = E + NI = E + X + I
```

And we have a simplified accounting equation:

```
A + L + E’ = 0
```

If we were to adjust the signs for credits and debits (see previous section) and have sums that are all positive number, this becomes the familiar accounting equation:

```
Assets - Liabilities = Equity
```

As you can see, it’s much easier to just always add up the numbers.

## Plain-Text Accounting[](https://beancount.github.io/docs/the_double_entry_counting_method.html#plain-text-accounting "Permanent link")

Ok, so now we understand the method and what it can do for us, at least in theory. The purpose of a double-entry bookkeeping system is to allow you to replicate the transactions that occur in various real world accounts into a single, unified system, in a common representation, and to extract various views and reports from this data. Let us now turn our attention to how we record this data in practice.

This document talks about Beancount, whose purpose is “double-entry bookkeeping using text files.” Beancount implements a parser for a simple syntax that allows you to record transactions and postings. The syntax for an example transaction looks something like this:

```
2016-12-06 * "Biang!" "Dinner"
  Liabilities:CreditCard   -47.23 USD
  Expenses:Restaurants
```

You write many of declarations like these in a file, and Beancount will read it and create the corresponding data structures in memory.

**Verification.** After parsing the transactions, Beancount also verifies the rule of the double-entry method: it checks that the sum of the postings on all your transactions is zero. If you make a mistake and record a transaction with a non-zero balance, an error will be displayed.

**Balance Assertions.** Beancount allows you to replicate balances declared from external accounts, for example, a balance written on a monthly statement. It processes those and checks that the balances resulting from your input transactions match those declared balances. This helps you detect and find mistakes easily.

**Plugins.** Beancount allows you to build programs which can automate and/or process the streams of transactions in your input files. You can build custom functionality by writing code which directly processes the transaction stream.

**Querying & Reporting.** It provides tools to then process this stream of transactions to produce the kinds of reports we discussed earlier in this document.

There are a few more details, for example, Beancount allows you to track cost basis and make currency conversions, but that’s the essence of it.

## The Table Perspective[](https://beancount.github.io/docs/the_double_entry_counting_method.html#the-table-perspective "Permanent link")

Almost always, questions asked by users on the mailing-list about how to calculate or track some value or other can be resolved easily simply by thinking of the data as a long list of rows, some of which need to be filtered and aggregated. If you consider that all that we’re doing in the end is deriving “sums” of these postings, and that the attributes of transactions and postings are what allows us to filter subsets of postings, it always becomes very simple. In almost all the cases, the answer is to find some way to disambiguate postings to select them, e.g. by account name, by attaching some tag, by using some metadata, etc. It can be illuminating to consider how this data can be represented as a table.

Imagine that you have two tables: a table containing the fields of each Transaction such as date and description, and a table for the fields of each Posting, such as account, amount and currency, as well as a reference to its parent transaction. The simplest way to represent the data is to **join** those two tables, replicating values of the parent transaction across each of the postings.

For example, this Beancount input:

```
2016-12-04 * "Christmas gift"
  Liabilities:CreditCard       -153.45 USD
  Expenses:Gifts

2016-12-06 * "Biang!" "Dinner"
  Liabilities:CreditCard   -47.23 USD
  Expenses:Restaurants

2016-12-07 * "Pouring Ribbons" "Drinks with friends"
  Assets:Cash     -25.00 USD
  Expenses:Tips     4.00 USD
  Expenses:Alcohol
```

could be rendered as a table like this:

| _**Date**_ | _**Fl**_ | _**Payee**_ | _**Narration**_ | _**Account**_ | _**Number**_ | _**Ccy**_ |
| --- | --- | --- | --- | --- | --- | --- |
| 2016-12-04 | \* |  | Christmas gift | Liabilities:CreditCard | \-153.45 | USD |
| 2016-12-04 | \* |  | Christmas gift | Expenses:Gifts | 153.45 | USD |
| 2016-12-06 | \* | Biang! | Dinner | Liabilities:CreditCard | \-47.23 | USD |
| 2016-12-06 | \* | Biang! | Dinner | Expenses:Restaurants | 47.23 | USD |
| 2016-12-07 | \* | Pouring Ribbons | Drinks with friends | Assets:Cash | \-25.00 | USD |
| 2016-12-07 | \* | Pouring Ribbons | Drinks with friends | Expenses:Tips | 4.00 | USD |
| 2016-12-07 | \* | Pouring Ribbons | Drinks with friends | Expenses:Alcohol | 21.00 | USD |

Notice how the values of Transaction fields are replicated for each posting. This is exactly like a regular database join operation. The posting fields begin at column “Account.” (Also note that this example table is simplified; in practice there are many more fields.)

If you had a joined table just like this you could filter it and sum up amounts for arbitrary groups of postings. This is exactly what the bean-query tool allows you to do: You can run an SQL query on the data equivalent to this in-memory table and list values like this:

```
SELECT date, payee, number WHERE account = "Liabilities:CreditCard";
```

Or sum up positions like this:

```
SELECT account, sum(position) GROUP BY account;
```

This simple last command generates the trial balance report.

Note that the table representation does not inherently constrain the postings to sum to zero. If your selection criteria for the rows (in the WHERE clause) always selects **_all_** the postings for each of the matching transactions, you are ensured that the final sum of all the postings is zero. If not, the sum may be anything else. Just something to keep in mind.

If you’re familiar with SQL databases, you might ask why Beancount doesn’t simply process its data in order to fill up an existing database system, so that the user could then use those database’s tools. There are two main reasons for this:

-   **Reporting Operations.** In order to generate income statements and balance sheets, the list of transactions needs to be preprocessed using the clear, open and close operations described previously. These operations are not trivial to implement in database queries and are dependent on just the report and ideally don’t need to modify the input data. We’d have to load up the posting data into memory and then run some code. We’re already doing that by parsing the input file; the database step would be superfluous.
    
-   **Aggregating Positions.** Though we haven’t discussed it in this document so far, the contents of accounts may contain different types of commodities, as well as positions with an attached cost basis. The way that these positions are aggregated together requires the implementation of a custom data type because it obeys some rules about how positions are able to cancel each other out (see [How Inventories Work](https://beancount.github.io/docs/how_inventories_work.html) for details). It would be very difficult to build these operations with an SQL database beyond the context of using just a single currency and ignoring cost basis.
    

This is why Beancount provides a custom tool to directly process and query its data: It provides its own implementation of an SQL client that lets you specify open and close dates and leverages a custom “Inventory” data structure to create sums of the positions of postings. This tools supports columns of Beancount’s core types: Amount, Position and Inventory objects.

(In any case, if you’re not convinced, Beancount provides a [tool](https://github.com/beancount/beancount/tree/v2/bin/bean-sql) to export its contents to a regular SQL database system. Feel free to experiment with it if you like, knock yourself out.)

[Martin Blais](mailto:blais@furius.ca), July 2014

[http://furius.ca/beancount/doc/getting-started](http://furius.ca/beancount/doc/getting-started)

## Introduction[](https://beancount.github.io/docs/getting_started_with_beancount.html#introduction "Permanent link")

This document is a gentle guide to creating your first Beancount file, initializing it with some options, some guidelines for how to organize your file, and instructions for declaring accounts and making sure their initial balance does not raise errors. It also contains some material on configuring the Emacs text editor, if you use that.

You will probably want to have read some of the [User’s Manual](https://beancount.github.io/docs/beancount_language_syntax.html) first in order to familiarize yourself with the syntax and kinds of available directives, or move on to the [Cookbook](https://beancount.github.io/docs/command_line_accounting_cookbook.html) if you’ve already setup a file or know how to do that. If you’re familiar with Ledger, you may want to read up on the [differences between Ledger and Beancount](https://beancount.github.io/docs/a_comparison_of_beancount_and_ledger_hledger.html) first.

## Editor Support[](https://beancount.github.io/docs/getting_started_with_beancount.html#editor-support "Permanent link")

Beancount ledgers are simple text files. You can use any text editor to compose your input file. However, a good text editor which understands enough of the Beancount syntax to offer focused facilities like syntax highlighting, autocompletion, and automatic indentation highly has the potential to greatly increase productivity in compiling and maintaining your ledger.

### Emacs[](https://beancount.github.io/docs/getting_started_with_beancount.html#emacs "Permanent link")

Support for editing Beancount ledger files in Emacs was traditionally distributed with Beancount. It now lives as its own project in [this Github repository](https://github.com/beancount/beancount-mode/).

### Vim[](https://beancount.github.io/docs/getting_started_with_beancount.html#vim "Permanent link")

Support for editing Beancount ledger files in Vim has been implemented by Nathan Grigg and is available in [this Github repository](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2Fnathangrigg%2Fvim-beancount&sa=D&sntz=1&usg=AFQjCNFgEjRsUHfpvOFxn8gD4-c_eK_wsA).

### Sublime[](https://beancount.github.io/docs/getting_started_with_beancount.html#sublime "Permanent link")

Support for editing with Sublime has been contributed by Martin Andreas Andersen and is available in [this github repository](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2Fdraug3n%2Fsublime-beancount&sa=D&sntz=1&usg=AFQjCNExx6wdX5QF1hnixgHcKJV-5XJwMA) or as a Sublime package [here](https://packagecontrol.io/packages/Beancount).

### VSCode[](https://beancount.github.io/docs/getting_started_with_beancount.html#vscode "Permanent link")

There are a number of plugins for working with Beancount text files including [VSCode-Beancount](https://marketplace.visualstudio.com/items?itemName=Lencerf.beancount) by Lencerf.

## Creating your First Input File[](https://beancount.github.io/docs/getting_started_with_beancount.html#creating-your-first-input-file "Permanent link")

To get started, let’s create a minimal input file with two accounts and a single transaction. Enter or copy the following input to a text file:

```
2014-01-01 open Assets:Checking
2014-01-01 open Equity:Opening-Balances

2014-01-02 * "Deposit"
  Assets:Checking           100.00 USD
  Equity:Opening-Balances
```

## Brief Syntax Overview[](https://beancount.github.io/docs/getting_started_with_beancount.html#brief-syntax-overview "Permanent link")

A few notes and an ultra brief overview of the Beancount syntax:

-   Currencies must be entirely in capital letters (allowing numbers and some special characters, like “\_” or “-”). Currency symbols (such as $ or €) are not supported.
    
-   Account names do not admit spaces (though you can use dashes), and must have at least two components, separated by colons. Each component of an account name must begin with a capital letter or number.
    
-   Description strings must be quoted, like this: `"AMEX PMNT"`.
    
-   Dates are only parsed in ISO8601 format, that is, YYYY-MM-DD.
    
-   Tags must begin with “#”, and links with “^”.
    

For a complete description of the syntax, visit the [User’s Manual](https://beancount.github.io/docs/beancount_language_syntax.html).

## Validating your File[](https://beancount.github.io/docs/getting_started_with_beancount.html#validating-your-file "Permanent link")

The purpose of Beancount is to produce reports from your input file (either on the console or serve via its web interface). However, there is a tool that you can use to simply load its contents and make some validation checks on it, to ensure that your input does not contain errors. Beancount can be quite strict; this is a tool that you use while you’re entering your data to ensure that your input file is legal. The tool is called “bean-check” and you invoke it like this:

```
bean-check /path/to/your/file.beancount
```

Try it now on the file you just created from the previous section. It should exit with no output. If there are errors, they will be printed on the console. The errors are printed out in a format that Emacs recognizes by default, so you can use Emacs’ `next-error` and `previous-error` built-in functions to move the cursor to the location of the problem.

## Viewing the Web Interface[](https://beancount.github.io/docs/getting_started_with_beancount.html#viewing-the-web-interface "Permanent link")

A convenient way to view reports is to bring up the “bean-web” tool on your input file. Try it:

```
bean-web /path/to/your/file.beancount
```

You can then point a web browser to [http://localhost:8080](http://localhost:8080/) and click your way around the various reports generated by Beancount. You can then modify the input file and reload the web page your browser is pointing to—bean-web will automatically reload the file contents.

At this point, you should probably read some of the [Language Syntax](https://beancount.github.io/docs/beancount_language_syntax.html) document.

## How to Organize your File[](https://beancount.github.io/docs/getting_started_with_beancount.html#how-to-organize-your-file "Permanent link")

In this section we provide general guidelines for how to organize your file. This assumes you’ve read the [Language Syntax](https://beancount.github.io/docs/beancount_language_syntax.html) document.

### Preamble to your Input File[](https://beancount.github.io/docs/getting_started_with_beancount.html#preamble-to-your-input-file "Permanent link")

I recommend that you begin with just a single file<sup id="fnref:1"><a href="https://beancount.github.io/docs/getting_started_with_beancount.html#fn:1">1</a></sup>. My file has a header that tells Emacs what mode to open the file with, followed by some common options:

```
;; -*- mode: beancount; coding: utf-8; fill-column: 400; -*-
option "title" "My Personal Ledger"
option "operating_currency" "USD"
option "operating_currency" "CAD"
```

The title option is used in reports. The list of “operating currencies” identify those commodities which you use most commonly as “currencies” and which warrant rendering in their own dedicated columns in reports (this declaration has no other effect on the behavior of any of the calculations).

### Sections & Declaring Accounts[](https://beancount.github.io/docs/getting_started_with_beancount.html#sections-declaring-accounts "Permanent link")

I like to organize my input file in sections that correspond to each real-world account. Each section defines all the accounts related to this real-world account by using an Open directive. For example, this is a checking account:

```
2007-02-01 open Assets:US:BofA:Savings              USD
2007-02-01 open Income:US:BofA:Savings:Interest     USD
```

I like to declare the currency constraints as much as possible, to avoid mistakes. Also, note how I declare an income account specific to this account. This helps break down income in reporting for taxes, as you will likely receive a tax document in relation to that specific account’s income (in the US this would be a 1099-INT form produced by your bank).

Here’s what the opening accounts might look like for an investment account:

```
2012-03-01 open Assets:US:Etrade:Main:Cash            USD
2012-03-01 open Assets:US:Etrade:Main:ITOT            ITOT
2012-03-01 open Assets:US:Etrade:Main:IXUS            IXUS
2012-03-01 open Assets:US:Etrade:Main:IEFA            IEFA
2012-03-01 open Income:US:Etrade:Main:Interest        USD
2012-03-01 open Income:US:Etrade:Main:PnL             USD
2012-03-01 open Income:US:Etrade:Main:Dividend        USD
2012-03-01 open Income:US:Etrade:Main:DividendNoTax   USD
```

The point is that all these accounts are related somehow. The various sections of the cookbook will describe the set of accounts suggested to create for each section.

Not all sections have to be that way. For example, I have the following sections:

-   **Eternal accounts.** I have a section at the top dedicated to contain special and “eternal” accounts, such as payables and receivables.
    
-   **Daybook.** I have a “daybook” section at the bottom that contains all cash expenses, in chronological order.
    
-   **Expense accounts.** All my expenses accounts (categories) are defined in their own section.
    
-   **Employers.** For each employer I’ve defined a section where I put the entries for their direct deposits, and track vacations, stock vesting and other job-related transactions.
    
-   **Taxes.** I have a section for taxes, organized by taxation year.
    

You can organize it any way you like, because Beancount doesn’t care about the ordering of declarations.

### Closing Accounts[](https://beancount.github.io/docs/getting_started_with_beancount.html#closing-accounts "Permanent link")

If a real-world account has closed, or is never going to have any more transactions posted to it, you can declare it “closed” at a particular date by using a Close directive:

```
; Moving to another bank.
2013-06-13 close Assets:US:BofA:Savings
```

This tells Beancount not to show the account in reports that don’t include any date where it was active. It also avoids errors by triggering an error if you do try to post to it at a later date.

## De-duping[](https://beancount.github.io/docs/getting_started_with_beancount.html#de-duping "Permanent link")

One problem that will occur frequently is that once you have [some sort of code or process](https://beancount.github.io/docs/importing_external_data.html) set up to automatically extract postings from downloaded files, you will end up importing postings which provide two separate sides of the same transaction. An example is the payment of a credit card balance via a transfer from a checking account. If you download the transactions for your checking account, you will extract something like this:

```
2014-06-08 * "ONLINE PAYMENT - THANK YOU"
  Assets:CA:BofA:Checking           -923.24 USD
```

The credit card download will yield you this:

```
2014-06-10 * "AMEX EPAYMENT    ACH PMT"
  Liabilities:US:Amex:Platinum       923.24 USD
```

Many times, transactions from these accounts need to be booked to an expense account, but in this case, these are two separate legs of the same transaction: a transfer. When you import one of these, you normally look for the other side and merge them together:

```
;2014-06-08 * "ONLINE PAYMENT - THANK YOU"
2014-06-10 * "AMEX EPAYMENT    ACH PMT"
  Liabilities:US:Amex:Platinum       923.24 USD
  Assets:CA:BofA:Checking           -923.24 USD
```

I often leave one of the description lines in comments—just my choice, Beancount ignores it. Also note that I had to choose one of the two dates. I just choose the one I prefer, as long as it does not break any balance assertion.

In the case that you would forget to merge those two imported transactions, worry not! That’s what balance assertions are for. Regularly place a balance assertion in either of these accounts, e.g., every time you import, and you will get a nice error if you end up entering the transaction twice. This is pretty common and after a while it becomes second nature to interpret that compiler error and fix it in seconds.

Finally, when I know I import just one side of these, I select the other account manually and I mark the posting I know will be imported later with a flag, which tells me I haven’t de-duped this transaction yet:

```
2014-06-10 * "AMEX EPAYMENT    ACH PMT"
  Liabilities:US:Amex:Platinum       923.24 USD
  ! Assets:CA:BofA:Checking
```

Later on, when I import the checking account’s transactions and go fishing for the other side of this payment, I will find this and get a good feeling that the world is operating as it should.

(If you’re interested in more of a discussion around de-duplicating and merging transactions, see this [feature proposal](https://beancount.github.io/docs/settlement_dates_in_beancount.html). Also, you might be interested in the [“effective\_date” plugin](https://www.google.com/url?q=https://github.com/redstreet/beancount_plugins_redstreet&sa=D&ust=1458615376548000&usg=AFQjCNGY-CWtCRP75-3p8Yr02BC_itG76g) external contribution, which splits transactions in two.)

### Which Side?[](https://beancount.github.io/docs/getting_started_with_beancount.html#which-side "Permanent link")

So if you organize your account in sections the way I suggest above, which section of the file should you leave such “merged” transactions in, that is, transactions that involve two separate accounts? Well, it’s your call. For example, in the case of a transfer between two accounts organized such that they have their own dedicated sections, it would be nice to be able to leave both transactions there so that when you edit your input file you see them in either section, but unfortunately, the transaction must occur in only one place in your document. You have to choose one.

Personally I’m a little careless about being consistent which of the section I choose to leave the transaction in; sometimes I choose one section of my input file, or that of the other account, for the same pair of accounts. It hasn’t been a problem, as I use Emacs and i-search liberally which makes it easy to dig around my gigantic input file. If you want to keep your input more tidy and organized, you could come up with a rule for yourself, e.g. “credit card payments are always left in the paying account’s section, not in the credit card account’s section”, or perhaps you could leave the transaction in both sections and comment one out<sup id="fnref:2"><a href="https://beancount.github.io/docs/getting_started_with_beancount.html#fn:2">2</a></sup>.

## Padding[](https://beancount.github.io/docs/getting_started_with_beancount.html#padding "Permanent link")

If you’re just starting out—and you probably are if you’re reading this—you will have no historical data. This means that the balances of your Assets and Liabilities accounts in Beancount will all be zero. But the first thing you should want to do after defining some accounts is establish a balance sheet and bring those amounts to their actual current value.

Let’s take your checking account as an example, say you opened it a while back. You don’t remember exactly when, so let’s use an approximate date:

```
2000-05-28 open Assets:CA:BofA:Checking  USD
```

The next thing you do is look up your current balance and put a balance assertion for the corresponding amount:

```
2014-07-01 balance Assets:CA:BofA:Checking    1256.35 USD
```

Running Beancount on just this will correctly produce an error because Beancount assumes an implicit balance assertion of “empty” at the time you open an account. You will have to “pad” your account to today’s balance by inserting a _balance adjustment_ at some point in time between the opening and the balance, against some equity account, which is an arbitrary place to book “where you received the initial balance from.” For this purpose, this is usually the “`Equity:Opening-Balances`” account. So let’s include this padding transaction and recap what we have so far:

```
2000-05-28 open Assets:CA:BofA:Checking  USD

2000-05-28 * "Initialize account"
  Equity:Opening-Balances                    -1256.35 USD
  Assets:CA:BofA:Checking                     1256.35 USD

2014-07-01 balance Assets:CA:BofA:Checking    1256.35 USD
```

From here onwards, you would start adding entries reflecting everything that happened after 7/1. However, what if you wanted to go _back_ in time? It is perfectly reasonable that once you’ve got your chart-of-accounts set up you might want to fill in the missing history until at least the beginning of this year.

Let’s assume you had a single transaction in June 2014, and let’s add it:

```
2000-05-28 open Assets:CA:BofA:Checking  USD

2000-05-28 * "Initialize account"
  Equity:Opening-Balances                    -1256.35 USD
  Assets:CA:BofA:Checking                     1256.35 USD

2014-06-28 * "Paid credit card bill"
  Assets:CA:BofA:Checking                     -700.00 USD
  Liabilities:US:Amex:Platinum                 700.00 USD

2014-07-01 balance Assets:CA:BofA:Checking    1256.35 USD
```

Now the balance assertion fails! You would need to adjust the initialization entry to fix this:

```
2000-05-28 open Assets:CA:BofA:Checking  USD

2000-05-28 * "Initialize account"
  Equity:Opening-Balances                    -1956.35 USD
  Assets:CA:BofA:Checking                     1956.35 USD

2014-06-28 * "Paid credit card bill"
  Assets:CA:BofA:Checking                     -700.00 USD
  Liabilities:US:Amex:Platinum                 700.00 USD

2014-07-01 balance Assets:CA:BofA:Checking    1256.35 USD
```

Now this works. So basically, every single time you insert an entry in the past, you would have to adjust the balance. Isn’t this annoying? Well, yes.

Fortunately, we can provide some help: you can use a Pad directive to replace and automatically synthesize the balance adjustment to match the next balance check, like this:

```
2000-05-28 open Assets:CA:BofA:Checking  USD

2000-05-28 pad Assets:CA:BofA:Checking Equity:Opening-Balances

2014-06-28 * "Paid credit card bill"
  Assets:CA:BofA:Checking                     -700.00 USD
  Liabilities:US:Amex:Platinum                 700.00 USD

2014-07-01 balance Assets:CA:BofA:Checking    1256.35 USD
```

Note that this is only needed for balance sheet accounts (Assets and Liabilities) because we don’t care about the initial balances of the Income and Expenses accounts, we only care about their transitional value (the changes they post during a period). For example, it makes no sense to bring up the Expenses:Restaurant account to the sum total value of all the costs of the meals you consumed since you were born.

So you will probably want to get started with Open & Pad directives for each Assets and Liabilities accounts.

## What’s Next?[](https://beancount.github.io/docs/getting_started_with_beancount.html#whats-next "Permanent link")

At this point you will probably move onwards to the [Cookbook](https://beancount.github.io/docs/command_line_accounting_cookbook.html), or read the [User’s Manual](https://beancount.github.io/docs/beancount_language_syntax.html) if you haven’t already done that.