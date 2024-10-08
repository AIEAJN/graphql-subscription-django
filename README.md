# graphql-subscription-django
This repository illustrates how to implement a GraphQL subscription using Django signals in a Django application, using the graphene-django and graphene-luna libraries.

# What is subscription?
In GraphQL, a subscription allows clients to receive real-time updates on specific events.

# API URL
```
https://subscription.meetsum.net/graphql
```

# Subscription example
```
subscription subscribeToNewManga {
  newManga {
    id
    name
    synopsis
    author
    createdDate
  }
}
```

# Mutation to add new manga
```
mutation addManga($name: String = "Bleach", $synopsis: String = "Synopsis", $author: String = "Tite Kubo") {
  addManga(name: $name, synopsis: $synopsis, author: $author) {
    success
    message
    manga {
      id
      name
      synopsis
      author
      createdDate
    }
  }
}
```

# Good to know
To test on GraphiQL, open two browser windows: one to run the subscription, which will listen for newly added manga, and the other to run the add manga mutation.