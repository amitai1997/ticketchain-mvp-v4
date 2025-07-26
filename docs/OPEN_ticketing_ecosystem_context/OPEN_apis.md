

<!-- Source file: ./apis/Concepts/a-concepts-overview.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Overview

Description: What is the Ticket Engine?
The Ticket Engine provides a way to programmatically register events and ticket interactions within OPN Ticketing Ecosystem with ease and is the primary interface for writing changes to the blockchain NFT state.
Writing data to the blockchain directly can be challenging du…

What is the Ticket Engine?

------------------------------

The **Ticket Engine** provides a way to programmatically register events and ticket interactions within OPN Ticketing Ecosystem with ease and is the primary interface for writing changes to the blockchain NFT state.

Writing data to the blockchain directly can be challenging due to some lack of guarantees, as well as knowledge of lower-layer implementation detail. Ticket Engine abstracts away the complexity of managing blockchain transactions yourself and provides cleaner, more convenient interfaces for using your event and ticket data.

Through experience we've learned that minting NFTs onto any blockchain represents a serious challenge and software expertise orthogonal to building successful ticketing software. By offering a simple HTTP API to creating NFT tickets on-chain it becomes easy to plug-in to your existing ticketing platforms.

> 👍
>
> ###
>
> Use the Ticket Engine to:
>
> *    Register your events on the blockchain.
> *    Define metadata for your events (start time, location, images...)
> *    Update your events.
> *    Register sold, resold, scanned, checked-in, and invalidated ticket interactions.
> *    Claim a ticket to a users' wallet.
> *    Define callback URLs to receive processing updates.
> *    Fetch information from a specific action.

A Digital Twin

------------------

The Ticket Engine API is designed to complement and add to your existing infrastructure rather than replacing it, so the tickets produced through this API integration are often referred to as a _digital twin_ of your primary ticket instance.

This provides a mechanism to issue blockchain-based NFT tickets without impacting your primary ticketing infrastructure or migrating any source of truth unless desired. Twinning your ticket inventory with a blockchain native copy allows you to explore the benefits of blockchain ticketing and expose these features to your users without adding additional operational-risk to your live system.

What information do we store?

---------------------------------

To not impose too strict of a model definition on the consumer, we only keep the necessary information needed on the blockchain itself. This allows for all base operations and interactions without inflating the blockchain state. Writing data to any blockchain operation is expensive so we attempt to minimise this for this reason also.

The three main entities exposed via the Ticket Engine API are _Events_, _Tickets_ , and _Metadata_, all of which can be written from the stream endpoint.

Ticket Engine - Simple ERD
```mermaid
flowchart LR
  subgraph Transaction["Transaction"]
    Event[Event]
    TicketA[Ticket]
    TicketB[Ticket]
    TicketA -->|eventId| Event
    TicketB -->|eventId| Event
  end
```


###

Events

Events are the entity which contains metadata on the virtual or real-world occasion, and is granted right of entry through the usage of a ticket and is not to be confused with a programmatic or blockchain event. Events have many tickets.

###

Tickets

Tickets define a right of access to an event. Association to this event is maintained by the `eventId` property on the ticket and this must be passed upon creation of a ticket.

###

Metadata

Unlike the above models that are defined by their domain model (in relation to the events industry), metadata can be optionally attached to a ticket. This can include metadata about the event itself but is more commonly used to define the primary NFT content & media.

Writes are handled asynchronously and an optional `callbackUrl` can be submitted with creation of an _Event_ so that the transaction hash and success status can be returned to you.

<!-- Source file: ./apis/Concepts/b-concepts-actions.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Actions

Description: The Ticket Engine API has been designed to accept a stream of actions, where each action is an operation that you wish to carry out on the protocol. Over time we've found that commercial ticketing applications often operate using message queues or event driven architectures and separating these acti…

The Ticket Engine API has been designed to accept a stream of actions, where each action is an operation that you wish to carry out on the protocol. Over time we've found that commercial ticketing applications often operate using message queues or event driven architectures and separating these actions into separate endpoints often adds additional overhead when it comes to implementation.

Offering a stream endpoint allows integrators on the protocol to forward mixed batches of action requests to the Ticket Engine API and these will be processed in the order they are received.

Action Types

----------------

Before any sold tickets can be registered on the protocol, you must first create an event as an `eventId` will be required when creating a ticket. The Ticket Engine API handles the ordering of transactions so there is no need to wait until the creation of an event has been confirmed on the blockchain, only that the event has been submitted to the Ticket Engine prior to registering the first sold ticket.

###

Events

There are two actions types available for interacting with events; `newEvent` and `updateEvent`, both of which require an `eventId`. This `eventId` is a client-side generated ID and can be a maximum of 255 characters in length.

The event ID must be unique to you but there are no restrictions on the content of this field it is possible to use your own existing event ID from your current ticketing systems as long as this uniqueness constraint is met. This event ID will not be propagated to the blockchain and is only used as a reference ID for Ticket Engine to use for subsequest requests.

*   `newEvent` will queue a transaction to create a new smart contract on the blockchain. This gives each event its own namespaced collection and separate blockchain address that can then be used within explorers, marketplaces, and other NFT tooling. All NFT tickets for that event will belong to the smart contract created using the `newEvent` action.
*   `updateEvent` will update the event's metadata on-chain. While we encourage customers to use as much transparency as possible when creating an event, the real-world can work differently. Event start and end times may be changed, names and headling acts may change, and the `updateEvent` action allows you to update the metadata stored on-chain for this event.

Event actions are unbilled and will not charge your account.

###

Tickets

As mentioned, a `newEvent` action must first be submitted to the API prior to registering a sold tickets. This can be done within the same request but it is necessary for the `eventId` to be present in the Ticket Engine prior to ticket processing.

There are a number of ticket actions available to change the state of a ticket on-chain:

*   `soldTicket` will create an NFT ticket within the event contract created as part of `newEvent`.
*   `resoldTicket` will log a secondary sale event on the ticket.
*   `scannedTicket` will issue a non-finalising scan event on a ticket. A scan can happen an unlimited amount of times and should be used for multi-day or multi-gate events.
*   `checkedInTicket` is a scan event that finalises the state of the ticket. For a single-gated event a check-in event should be used instead of a scan. Upon check-in the NFT is ready to be claimed into a user's wallet.
*   `invalidatedTicket` will also finalise the ticket's lifecycle although this will not enable claiming. To be used for event invalidations & cancellations.

Updating metadata does not affect blockchain storage:

*   `updateTicket` will change the NFT Content URI, which is the media file used on NFT marketplaces and wallets.

Ticket Lifecycle

--------------------

The Ticket Engine lifecycle attempts to be as flexible as possible so that it can accomodate all customer workflows, although there are some validations that occur between states.

The Event-Ticket Lifecycle
```mermaid
flowchart LR
  subgraph EventLifecycle["Event Lifecycle"]
    newEvent["newEvent"]
    updateEvent["updateEvent"]
    newEvent --> updateEvent
    updateEvent --> updateEvent
  end

  newEvent --> soldTicket

  subgraph TicketLifecycle["Ticket Lifecycle"]
    soldTicket["soldTicket"]
    resoldTicket["resoldTicket"]
    scannedTicket["scannedTicket"]
    checkedInTicket["checkedInTicket"]
    invalidatedTicket["invalidatedTicket"]
    claimedTicket["claimedTicket"]

    soldTicket --> resoldTicket
    resoldTicket --> resoldTicket
    resoldTicket --> scannedTicket
    scannedTicket --> checkedInTicket
    scannedTicket --> invalidatedTicket
    checkedInTicket --> claimedTicket
  end

  claimedTicket --> User["User"]
```

The most basic lifecycle for a sold ticket that is then validated upon entry and then claimed by a user would take the flow:

1.  `soldTicket` to create the NFT.
2.  `checkedInTicket` to finalise the lifecycle.
3.  `claimedTicket` to claim to a user's wallet.

Checked-in and invalidated tickets have already completed their lifecycle and cannot be further scanned or resold. Tickets cannot be resold after the first scan is registered. Claiming is only possible for checked-in tickets.

| Requested Action Type | Requires | Blocked On |
| --- | --- | --- |
| `undefined soldTicket` | `undefined newEvent` |  |
| `undefined resoldTicket` | `undefined soldTicket` | `undefined scannedTicket` `undefined checkedInTicket` `undefined invalidatedTicket` `undefined claimedTicket` |
| `undefined scannedTicket` | `undefined soldTicket` | `undefined checkedInTicket` `undefined invalidatedTicket` `undefined claimedTicket` |
| `undefined scannedTicket` | `undefined soldTicket` | `undefined checkedInTicket` `undefined invalidatedTicket` `undefined claimedTicket` |
| `undefined checkedInTicket` | `undefined soldTicket` | `undefined checkedInTicket` `undefined invalidatedTicket` `undefined claimedTicket` |
| `undefined invalidatedTicket` | `undefined soldTicket` | `undefined checkedInTicket` `undefined invalidatedTicket` `undefined claimedTicket` |
| `undefined claimedTicket` | `undefined soldTicket` `undefined checkedInTicket` | `undefined invalidatedTicket` `undefined claimedTicket` |
> 👍
>
> ###
>
> Recap
>
> *    Ticket Engine will handle queuing, no need to wait for blockchain confirmations.
> *    An event must be submitted to the API before registering the first sold ticket.
> *    Full schema for each action type can be found within the stream endpoint documentation.
> *    Event actions are not billed. Sold tickets will be billed upon blockchain confirmation.
> *    Reselling or scanning is not available for checked-in or invalidated tickets.
> *    Claiming is only possible for checked-in tickets.

<!-- Source file: ./apis/Concepts/c-concepts-event-contracts.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Event Contracts

Description: Routing to a Ticket
Locating a ticket on OPN Ticketing Ecosystem can be done using three components:

The blockchain network it is issued on, e.g. "POLYGON".
The index of the event it belongs to, e.g. "2".
The index of the NFT within that event, e.g. "3"

Bringing those three values together creates…

Routing to a Ticket

-----------------------

Locating a ticket on OPN Ticketing Ecosystem can be done using three components:

*   The blockchain network it is issued on, e.g. "POLYGON".
*   The index of the event it belongs to, e.g. "2".
*   The index of the NFT within that event, e.g. "3"

Bringing those three values together creates a composite key for each unique ticket knows as the `nftId` and this is guaranteed to be unique across all tickets on all blockchain networks. Using the example above would yield a complete `nftId` of `POLYGON-2-3`, meaning this is the third NFT ticket, on the second event, on the Polygon network.

Data heirarchy of Blockchain > Event > Ticket (NFT)
```mermaid
flowchart LR
  E1[Event 1]
  MC1["Event 1 NFT Ticket Contract\n0x7a7..."]
  subgraph Coll1["Marketplace Collections – 0x7a7..."]
    Asset1["NFT Ticket 12"]
    Des1(("Low effort, no community access, no utility, basic art"))
  end
  E1 -->|Mint| MC1
  MC1 --> Coll1
  Asset1 -.-> Des1

  E2[Event 2]
  MC2["Event 2 NFT Ticket Contract\n0x8a8..."]
  subgraph Coll2["Marketplace Collections – 0x8a8..."]
    Asset2["NFT Ticket 3"]
    Des2(("High quality art, very rare, high value, community access & perks"))
  end
  E2 -->|Mint| MC2
  MC2 --> Coll2
  Asset2 -.-> Des2

  E3[Event 3]
  MC3["Event 3 NFT Ticket Contract\n0x9a9..."]
  subgraph Coll3["Marketplace Collections – 0x9a9..."]
    Asset3["NFT Ticket 2851"]
    Des3(("Private ticket & event, no metadata, no art"))
  end
  E3 -->|Mint| MC3
  MC3 --> Coll3
  Asset3 -.-> Des3
```

Upon success confirmation, the Actions endpoint returns both the complete `nftId` as well as the native smart contract address within the `eventAddress` field. It is this event address that is the most useful for composition with third-party tooling.

Interacting with an Event Contract

--------------------------------------

NFT collections are defined by the smart contract address that created the NFT and because each real-world event is created on-chain with its own unique smart contract address, keeping NFT collections for each separate event is straightforward.

For example, if an action returns an `eventAddress` of `0x3F2FBa6028f833E17C8087c385A4Ef4fc52F62bf` on the Polygon network, then this can be used to:

*   View the event directly on PolygonScan.
*   Browse the NFT collection on OpenSea.
*   Create a space on Snapshot, to allow NFT ticket holders to vote on proposals.
*   Offer private community & discussion forums to attendees using CollabLand.

Web3 is known for its composability, and because each ticket issued on OPN Ticketing Ecosystem is compatible to the ERC-721 standard, it becomes easy to 'plug-in' to emerging platforms and offer a more engaging pre-and-post-event fan experience.

<!-- Source file: ./apis/Concepts/d-concepts-nft-content.md -->

---
### ⚡️ ==================== ⚡️
---

Title: NFT Content

Description: The popularity of an NFT is largely driven by the imagery and media content it displays in NFT marketplaces and wallet applications.
As a user of the Ticket Engine you are in control over the image and multimedia content of your NFT tickets and we provide the updateTicket action to allow you to upda…

The popularity of an NFT is largely driven by the imagery and media content it displays in NFT marketplaces and wallet applications.

As a user of the Ticket Engine you are in control over the image and multimedia content of your NFT tickets and we provide the `updateTicket` action to allow you to update the URI reference which points to your image asset. At present, hosting of the image assets at this URI would remain the responsibility of the integrator.

Accepted Formats

--------------------

We support all image and video filetypes commonly used as NFT content and the API will not restrict updates based on filetype:

*   JPG
*   PNG
*   GIF
*   MP4
*   WEBM

Note however that support for display will depend on browser compatibility and content should be checked prior to updating. This is important as most NFT collectors will be using a web browser to explore marketplace collections.

Although we do not set a limit on the filesize as this is hosted within your own storage, be aware that NFT marketplaces may place size restictions on multimedia content due to how they ingest and cache this data. For that reason we do not recommend exceeding 100MB in file size.

On-chain Referencing

------------------------

The Metadata endpoint is compatible with the OpenSea Metadata Standards. Each NFT has its own unique public JSON metadata endpoint and this can be seen by calling the `tokenURI(uint256 _tokenId)` for the contract address for each event.

<!-- Source file: ./apis/Concepts/e-ticket-engine-privacy.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Privacy

Description: Through our own experience working directly with event organisers and artists we understand that not all information can be made public the moment the first ticket is sold and some events require some level of privacy and this is supported.
Transparency remains at the heart of the protcol and as suc…

Through our own experience working directly with event organisers and artists we understand that not all information can be made public the moment the first ticket is sold and some events require some level of privacy and this is supported.

Transparency remains at the heart of the protcol and as such usage of private or null data is only recommended when necessary.

Workflow Example

--------------------

> As an _event organiser_ I want to _hide the name of my event_ so that _I don't pre-announce prior to marketing readiness_.

Crucially, the Ticket Engine will only publish what you send to it, so the recommended workflow is the simplest; don't send what you aren't ready to publish. Due to data validation in earlier versions of the engine we found that integrators would often send a hashed or encrypted string for the event name, but this is no longer required. Leaving this blank allows us to display default information on the Ticket Explorer and results in less garbage on-chain.

Firstly you can create the event with only the fields you wish to submit:

JSON

```
[
{
"action": "newEvent",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"currency": "EUR",
"startTime": 1652285087,
"endTime": 1652285087,
"callbackUrl": "http://callback.url/callback"
}
}
]
```

And when you have received an all-clear from the event organiser or marketing team in this scenario you are able to issue an `updateEvent` action to fill the missing fields:

JSON

```
[
{
"action": "updateEvent",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"eventName": "Embargo No-More: A Night in Concert",
"shopUrl": "http://example.com",
"imageUrl": "https://placeimg.com/640/480/nature",
"latitude": -24.2066,
"longitude": -159.3224
}
}
]
```

> 📘
>
> ###
>
> The API cannot publish what it is not provided.
>
> We've taken care to ensure that only the bare-minimum fields are required allowing for sane fallbacks or `null` values to be used instead. Any data that is not provided cannot be published to the blockchain and this is the preferred route for events that have privacy constraints.

<!-- Source file: ./apis/Concepts/f-ticket-engine-asynchronous-confirmation.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Asynchronous Confirmation

Description: The underlying blockchain environment is public and competitive, and the available resource space for confirming transactions can be limited even on the most advanced chains. During times when the network is under high load returning a transaction confirmation within the HTTP response timeout is not…

The underlying blockchain environment is public and competitive, and the available resource space for confirming transactions can be limited even on the most advanced chains. During times when the network is under high load returning a transaction confirmation within the HTTP response timeout is not feasible, so for this reason should be treated as an asynchronous operation in all cases and the API is designed as such.

Blockchain Primer

---------------------

Consistently writing transactions at scale onto any blockchain is not an easy task, and avoiding this effort may be one of the reasons you're considering GET Protocol. The Ticket Engine abstracts away a lot of the mayhem, but it is still worth having a surface level understanding of the primitives beneath and how they can affect the system architecture above.

High-Level Ticket-Engine Architecture
```mermaid
flowchart LR
  API["API Requests"]

  subgraph GETProtocol["GET Protocol"]
    TE["Ticket Engine"]
    BN["Blockchain Node"]
  end

  subgraph BlockchainNetwork["Blockchain Network"]
    V1["Validator"]
    V2["Validator"]
    V3["Validator"]
  end

  API --> TE
  TE --> BN
  BN --> V1
  BN --> V2
  BN --> V3
```

###

Transactions

All interactions with a blockchain happen through transactions. These aren't necessarily financial transactions or involve transacting money to another party, rather the terminology here is similar to a database transaction. All writes to a blockchain network happens via these transactions. When a transaction is confirmed the blockchain generates and returns a `transactionHash` or `txHash` unique to that transaction.

The Polygon and Ethereum documentation covers these in more depth:

*   Polygon Developer Documentation
*   Ethereum Developer Documentation

Blockchains are notoriously competitive environments and parties all over the world are attempting to have their transactions confirmed with limited throughput available for everyone. This is handled by the gas fee market which allows people to bid higher amounts to have their transactions included more quickly.

GET Protocol handles this by using a number of pricing algorithms and intelligent batching transactions to ensure cost effectiveness as well as quick confirmation. Out NFT smart contracts are highly gas optimised to result in the best possible throughput needed for high volume ticket sales.

###

Guarantees

Since the transaction confirmation time cannot be guaranteed it would not be feasible to return a blockchain-generated `txHash` in the response body of each Ticket Engine request. Instead we offer our own hash that represents _a promise on the confirmation of a given action_, which you can find as `actionPromise` in the response. This is returned instantly with each request made and can be queried against the actions endpoint to retrieve the status of a request as well as additional blockchain information.

Recieving Transaction Confirmations

---------------------------------------

There are two mechanisms available for receiving the blockchain confirmation and `txHash` of the transaction:

###

Polling

By using the `actionPromise` returned for every action, polling for blockchain confirmation status becomes possible by using Actions with the received `actionPromise` parameter. Once confirmed will return the blockchain `txHash` that can then be viewed on a blockchain explorer as well as the `eventAddress` that represents the smart contract address for that event, and the `tokenId` of the NFT the action related to.

Although it is possible to poll the Actions endpoint for confirmation statuses we recommend setting up a webhook for real-time and time-sensitive confirmations. Where webhooks are not possible we recommend using a back-off strategy to avoid excess requests.

###

Webhooks / Callbacks

All submitted actions will receive a `actionPromise` in the response body, but events that have been created with a `callbackUrl` will also receive a callback to the URL provided with this promise ID. For event-driven systems this offers you the ability to offer your users notification of ticket confirmation in real-time as you will only recieve the callback when there is updated data ready to be fetched.

Since the callback includes the `promise` ID, you are then able to use this to request the updated data from the Actions endpoint.

See the Callbacks section for more information on the structure of the data passed to the `callbackUrl`

Designing your Webhooks

---------------------------

A unique `callbackUrl` can be defined per-event and all transactions related to that event will be returned to that URL. Confirmations for the tickets associated to that event will also go to the event `callbackUrl`. The webhook must be secured using HTTPS for the request to be made.

Since the webhook URL can be unique to each event created on the Ticket Engine and is not stored publicly on-chain you may wish to consider:

*   Adding the eventId to the URL. The `eventId` is passed as JSON so this isn't required, but you would more easily be able to restrict access and deprecate the endpoint when your event is finished using your application routing.
*   Passing an access key as part of the query string. The callback will be sent to the full URL so this would allow you to add a separate token to the URL which will be respected when the callback is sent.

###

Examples

*   `https://api.myticketcompany.com/events/<eventId>/nft_webhook`
*   `https://www.acme.events/hooks/<eventId>?token=<token>`

###

Retries & Successes

The callback will use an exponential back-off for timing and will make a **total of 5 attempts** to receive a successful `200 OK` response from the webhook API.

<!-- Source file: ./apis/Ticket Engine API V2/a-ticket-engine-environments.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Environments

Description: We offer two environments for integration, a playground (sandbox) and production.

Playground: https://engine.play.onopen.xyz
Production: https://engine.onopen.xyz

Each environment will require a separate API key and this will be provided.
Playground Environment
The playground environment is intend…

We offer two environments for integration, a playground (sandbox) and production.

*   Playground: `https://engine.play.onopen.xyz`
*   Production: `https://engine.onopen.xyz`

Each environment will require a separate API key and this will be provided.

Playground Environment

--------------------------

The playground environment is intended to be used as a self contained test environment for your integration with the Ticket Engine API. Playground transactions are unmetered and will not be billed.

To offer a production-like environment, all transactions generated by this environment will happen on the public `mainnet` of the blockchain network although no real OPN funds will be used. Data on the public mainnet is still public and accessible to anyone through blockchain explorers so usage of mock data is highly recommended.

Because this uses the mainnet blockchain network transactions you make will require real funds to initiate transactions at the network level. The Ticket Engine abstracts away the complexity of managing these blockchain account balances but we do not recommend running extended stress-tests on the playground environment.

Production Environment

--------------------------

The production environment will also write transactions to the public blockchain `mainnet`. Like playground, expect everything written to the mainnet to be immutable and as such should be treated with care. The production environment has been optimised for high-volume ticket sales and is designed to handle all load profiles.

Prior to registering sold tickets on production you will first need to top-up your account from within the Integrator Dashboard to fund NFT minting on the protocol.

Subgraph

------------

It is possible to query on-chain records directly using the OPN Ticketing Ecosystem Subgraph, hosted on TheGraph. This service indexes all OPN Ticketing Ecosystem blockchain events into a GraphQL interface and data store that updates in real-time. It is possible to query this Subgraph to assess blockchain-level information:

*   Polygon (Production)

The Subgraph is open-source and further documentation on how to use it is available on the Github repository.

Blockchain Explorers

------------------------

Once you have started successfully sending requests to the Ticket Engine API the natural next step may be to check the blockchain records to see the transaction written to the chain. The easiest way to do this would be to access the Ticket Explorer to view your transactions being written in real-time. Take a look at the Ticket Explorer Environments to access the explorer for your environment.

After finding the ticket that you have just created, you can navigate through to the ticket timeline page and then find a link to the blockchain explorer transaction for the request submitted.

Polygonscan is the recommended explorer for Polygon mainnet and inputting the `txHash` for a given action will return the batch in which that action was committed to the blockchain.

<!-- Source file: ./apis/Ticket Engine API V2/b-ticket-engine-development.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Development

Description: We first recommend developing an integration against the playground environment to test your implementation before attempting to integrate with the production environment. While the playground environment is designed to behave as closely to production as possible, minting real NFTs, it is not billed…

We first recommend developing an integration against the `playground` environment to test your implementation before attempting to integrate with the production environment. While the playground environment is designed to behave as closely to production as possible, minting real NFTs, it is not billed and it is safe to create test events.

You are free to use the playground environment in your own development, testing, or staging environments.

Verifying An Action

-----------------------

> 📘
>
> After creating an event or ticket on the Ticket Engine API you may wish to verify that your integration is successful. There are two ways to do this:
>
> *   Using the actions API endpoint.
> *   Checking the blockchain records.
> *   Looking for updates to the Ticket Explorer.

###

Using the API

When making calls to the /stream endpoint you will have the option to provide a `callbackUrl` when creating an event. Whenever there is a status update available, a POST request will be sent to this URL containing a promise UUID that you can use to query /actions

If a `callbackUrl` was not provided, you will also have been returned an `actionPromise` in the body of the /stream response. This can be used to query /actions periodically for updates. This process is detailed more within the Asynchronous Confirmation page.

###

Using the Blockchain

It is also possible to query the blockchain directly using the Subgraph as this will automatically index new blockchain records in real-time as transactions are confirmed. If you wish to ensure that the blockchain records are being created successfully you can query the Subgraph.

Each record on-chain will be associated to your integrator ID that will have been provided as part of onboarding. Should you need to find this again using the Subgraph, this is possible with the following query:

GraphQL

```
{
integrators {
id
name
}
}
```

Once you have your ID (below, "1") is is then possible to write a query to see your most recently created events, the tickets associated with that event, as well as any actions that have occurred on each ticket:

GraphQL

```
{
events(where: { integrator: "1" }, orderBy: blockTimestamp, orderDirection: desc) {
id
eventIndex
name
tickets(orderBy: blockTimestamp, orderDirection: desc) {
id
tokenId
usageEvents {
type
txHash
}
}
}
}
```

###

Using the Ticket Explorer

The Ticket Explorer is used as a tool for ticket buyers to see more information about their ticket or understand more about the activity happening on OPN Ticketing Ecosystem. The Ticket Explorer updates in real-time and can act as a tool to view NFT tickets that you create.

Once an action has been confirmed you will be able to use the `nftId` and the `explorerUrl` from the /actions response to view the ticket on the explorer. The explorer URL can be opened in a web browser to show the history of actions on that ticket along with the links to the blockchain transactions.


<!-- Source file: ./apis/Ticket Engine API V2/c-ticket-engine-authentication.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Authentication

Description: 🚧If you haven't yet received your X-Api-Key token as part of your onboarding process then please contact support to resolve.
All API endpoints expect an X-Api-Key to be passed on each request as a header and you will receieve a separete API key for the production and playground environments.
How th…

> 🚧
>
> If you haven't yet received your `X-Api-Key` token as part of your onboarding process then please contact support to resolve.

All API endpoints expect an `X-Api-Key` to be passed on each request as a header and you will receieve a separete API key for the production and playground environments.

How these keys are stored is your decision but consider keeping these secrets outside of your codebase, possibly in an environment variable or a dedicated secrets module such as Vault or AWS Secrets Manager

Note that all requests must be sent over HTTPS.

cURLJavaScriptPython

```
curl -X POST 'https://engine.play.onopen.xyz/stream' \
-H 'X-Api-Key: <string, required>' \
-H 'Content-Type: application/json'
```

```
fetch("https://api.playground.engine.get-blockchain.io/stream", {
headers: {
"Content-Type": "application/json",
"X-Api-Key": "<string, required>"
},
method: "POST"
})
```

```
import requests

headers = {
'X-Api-Key': '<string, required>',
'Content-Type': 'application/json',
}

response = requests.post('https://api.playground.engine.get-blockchain.io/stream', headers=headers)
```

Authentication failures will be returned with a `403 Forbidden` status code and body:

JSON

```
{
"message": "Forbidden"
}
```

Key Rotation

----------------

Should you require a new key to be issued then please get in touch with your support contact who will assist you immediately. Key rotation through a self-service process is currently being worked on and updates will be provided as soon as this is ready.

<!-- Source file: ./apis/Ticket Engine API V2/d-ticket-engine-supported-currencies.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Supported Currencies

Description: 👍Transparancy in TicketingPricing information in the native currency of an event is important for the transparency and authenticity of a ticket. OPN Ticketing Ecosystem is actively working towards an open ticketing standard to offer buyers accurate and real-time information of their purchase.
Integ…

> 👍
>
> ###
>
> Transparancy in Ticketing
>
> Pricing information in the native currency of an event is important for the transparency and authenticity of a ticket. OPN Ticketing Ecosystem is actively working towards an open ticketing standard to offer buyers accurate and real-time information of their purchase.

Integrating

---------------

When creating a `newEvent` on the Ticket Engine API /stream endpoint you are required to provide a currency in the form of an ISO 4217 currency code. This should be set as the currency in which the majority of the tickets for this event are sold as this will be the currecy for the `price`field for the `soldTicket` and `resoldTicket` actions.

Note that multi-currency events are not supported at this time, and in these cases we recommend converting all sale prices to the most common currency offered before providing it to a `soldTicket` or `resoldTicket` action.

Suppored Currency Codes

---------------------------

*   AED: United Arab Emirates Dirham
*   AFN: Afghan Afghani
*   ALL: Albanian Lek
*   AMD: Armenian Dram
*   ANG: Netherlands Antillean Guilder
*   AOA: Angolan Kwanza
*   ARS: Argentine Peso
*   AUD: Australian Dollar
*   AWG: Aruban Florin
*   AZN: Azerbaijani Manat
*   BAM: Bosnia-Herzegovina Convertible Mark
*   BBD: Barbadian Dollar
*   BDT: Bangladeshi Taka
*   BGN: Bulgarian Lev
*   BHD: Bahraini Dinar
*   BIF: Burundian Franc
*   BMD: Bermudan Dollar
*   BND: Brunei Dollar
*   BOB: Bolivian Boliviano
*   BRL: Brazilian Real
*   BSD: Bahamian Dollar
*   BTN: Bhutanese Ngultrum
*   BWP: Botswanan Pula
*   BYN: Belarusian Ruble
*   BZD: Belize Dollar
*   CAD: Canadian Dollar
*   CDF: Congolese Franc
*   CHF: Swiss Franc
*   CLP: Chilean Peso
*   CNY: Chinese Yuan
*   COP: Colombian Peso
*   CRC: Costa Rican Colón
*   CUC: Cuban Convertible Peso
*   CUP: Cuban Peso
*   CVE: Cape Verdean Escudo
*   CZK: Czech Republic Koruna
*   DJF: Djiboutian Franc
*   DKK: Danish Krone
*   DOP: Dominican Peso
*   DZD: Algerian Dinar
*   EEK: Estonian Kroon
*   EGP: Egyptian Pound
*   ERN: Eritrean Nakfa
*   ETB: Ethiopian Birr
*   EUR: Euro
*   FJD: Fijian Dollar
*   FKP: Falkland Islands Pound
*   GBP: British Pound Sterling
*   GEL: Georgian Lari
*   GGP: Guernsey Pound
*   GHS: Ghanaian Cedi
*   GIP: Gibraltar Pound
*   GMD: Gambian Dalasi
*   GNF: Guinean Franc
*   GTQ: Guatemalan Quetzal
*   GYD: Guyanaese Dollar
*   HKD: Hong Kong Dollar
*   HNL: Honduran Lempira
*   HRK: Croatian Kuna
*   HTG: Haitian Gourde
*   HUF: Hungarian Forint
*   IDR: Indonesian Rupiah
*   ILS: Israeli New Sheqel
*   IMP: Manx pound
*   INR: Indian Rupee
*   IQD: Iraqi Dinar
*   IRR: Iranian Rial
*   ISK: Icelandic Króna
*   JEP: Jersey Pound
*   JMD: Jamaican Dollar
*   JOD: Jordanian Dinar
*   JPY: Japanese Yen
*   KES: Kenyan Shilling
*   KGS: Kyrgystani Som
*   KHR: Cambodian Riel
*   KMF: Comorian Franc
*   KPW: North Korean Won
*   KRW: South Korean Won
*   KWD: Kuwaiti Dinar
*   KYD: Cayman Islands Dollar
*   KZT: Kazakhstani Tenge
*   LAK: Laotian Kip
*   LBP: Lebanese Pound
*   LKR: Sri Lankan Rupee
*   LRD: Liberian Dollar
*   LSL: Lesotho Loti
*   LYD: Libyan Dinar
*   MAD: Moroccan Dirham
*   MDL: Moldovan Leu
*   MGA: Malagasy Ariary
*   MKD: Macedonian Denar
*   MMK: Myanma Kyat
*   MNT: Mongolian Tugrik
*   MOP: Macanese Pataca
*   MRU: Mauritanian Ouguiya
*   MTL: Maltese Lira
*   MUR: Mauritian Rupee
*   MVR: Maldivian Rufiyaa
*   MWK: Malawian Kwacha
*   MXN: Mexican Peso
*   MYR: Malaysian Ringgit
*   MZN: Mozambican Metical
*   NAD: Namibian Dollar
*   NGN: Nigerian Naira
*   NIO: Nicaraguan Córdoba
*   NOK: Norwegian Krone
*   NPR: Nepalese Rupee
*   NZD: New Zealand Dollar
*   OMR: Omani Rial
*   PAB: Panamanian Balboa
*   PEN: Peruvian Nuevo Sol
*   PGK: Papua New Guinean Kina
*   PHP: Philippine Peso
*   PKR: Pakistani Rupee
*   PLN: Polish Zloty
*   PYG: Paraguayan Guarani
*   QAR: Qatari Rial
*   RON: Romanian Leu
*   RSD: Serbian Dinar
*   RUB: Russian Ruble
*   RWF: Rwandan Franc
*   SAR: Saudi Riyal
*   SBD: Solomon Islands Dollar
*   SCR: Seychellois Rupee
*   SDG: Sudanese Pound
*   SEK: Swedish Krona
*   SGD: Singapore Dollar
*   SHP: Saint Helena Pound
*   SLL: Sierra Leonean Leone
*   SOS: Somali Shilling
*   SRD: Surinamese Dollar
*   SSP: South Sudanese Pound
*   STN: São Tomé and Príncipe Dobra
*   SVC: Salvadoran Colón
*   SYP: Syrian Pound
*   SZL: Swazi Lilangeni
*   THB: Thai Baht
*   TJS: Tajikistani Somoni
*   TMT: Turkmenistani Manat
*   TND: Tunisian Dinar
*   TOP: Tongan Paʻanga
*   TRY: Turkish Lira
*   TTD: Trinidad and Tobago Dollar
*   TWD: New Taiwan Dollar
*   TZS: Tanzanian Shilling
*   UAH: Ukrainian Hryvnia
*   UGX: Ugandan Shilling
*   USD: United States Dollar
*   UYU: Uruguayan Peso
*   UZS: Uzbekistan Som
*   VEF: Venezuelan Bolívar Fuerte
*   VND: Vietnamese Dong
*   VUV: Vanuatu Vatu
*   WST: Samoan Tala
*   XCD: East Caribbean Dollar
*   YER: Yemeni Rial
*   ZAR: South African Rand
*   ZMW: Zambian Kwacha

> 📘
>
> ###
>
> Don't see your currency?
>
> In rare instances when a currency isn't supported by the Ticket Engine API then we recommend converting prices to a supported one that would be commonly available to your ticket buyers (such as USD or EUR). Alternatively get in touch with any requirements to help us expand this list.

<!-- Source file: ./apis/Ticket Engine API V2/e-ticket-engine-api-stream.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Stream

```
POST https://engine.play.onopen.xyz/stream
```

Description: The POST /stream endpoint allows you to register actions on your events/tickets alongside all of their relevant metadata within OPEN Ticketing and propagate this data to the blockchain.
The accepted actions are:

newEvent
updateEvent
soldTicket
updateTicket
resoldTicket
scannedTicket
checkedInTicket…

The `POST /stream` endpoint allows you to register actions on your events/tickets alongside all of their relevant metadata within OPEN Ticketing and propagate this data to the blockchain.

The accepted actions are:

*   `newEvent`
*   `updateEvent`
*   `soldTicket`
*   `updateTicket`
*   `resoldTicket`
*   `scannedTicket`
*   `checkedInTicket`
*   `claimedTicket`
*   `invalidatedTicket`

An event must first be registered before any ticket action be accepted within that event.

Per action, the following fields are accepted:

*   Required Fields: all specified must be sent
*   Exclusive Fields: 1 required but no more than 1 accepted
*   Optional Fields: all can be omitted, defaults will be used (see `Data Field Types` table for defaults)

| action | required fields | exclusive fields | optional fields |
| --- | --- | --- | --- |
| `newEvent` | `eventId` `currency` |  | `eventName` `shopUrl` `coverImageUrl` `coverMediaUrl` `defaultNftImageUrl` `defaultNftMediaUrl` `latitude` `longitude` `startTime` `endTime` `callbackUrl` |
| `updateEvent` | `eventId` |  | `eventName` `currency` `shopUrl` `coverImageUrl` `coverMediaUrl` `defaultNftImageUrl` `defaultNftMediaUrl` `latitude` `longitude` `startTime` `endTime` `callbackUrl` |
| `soldTicket` | `eventId` `ticketId` `userId` `price` |  | `imageUrl` `mediaUrl` `orderTime` `to` `metadataAttributes` `name` `description` |
| `updateTicket` |  | `ticketId` `nftId` | `imageUrl` `mediaUrl` `metadataAttributes` |
| `resoldTicket` | `userId` `price` | `ticketId` `nftId` | `orderTime` `to` |
| `scannedTicket` |  | `ticketId` `nftId` | `orderTime` |
| `checkedInTicket` |  | `ticketId` `nftId` | `orderTime` |
| `claimedTicket` | `to` or `userId` (both also accepted) | `ticketId` `nftId` | `orderTime` |
| `invalidatedTicket` |  | `ticketId` `nftId` | `orderTime` |

Note: On `resoldTicket` actions, the `userId` should represent the user that has just bought the ticket. It must be a different user identifier from the user that held the ticket previous to the resale (sent in the previous `soldTicket` or `resoldTicket` action for that ticket)

###

Data Field Types

| data field | type | validation | default value | on blockchain? |
| --- | --- | --- | --- | --- |
| `eventId` | string | up to 255 chars | \- | no |
| `eventName` | string | up to 255 chars | blank string | yes |
| `currency` | string | ISO 4217, exactly 3 chars - see supported currencies | \- | yes |
| `shopUrl` | string | http/https url, up to 255 chars | blank string | yes |
| `coverImageUrl` | string | http/https url, up to 255 chars | blank string | yes |
| `coverMediaUrl` | string | http/https url, up to 255 chars | blank string | no |
| `defaultNftImageUrl` | string | http/https url, up to 255 chars | blank string | no |
| `defaultNftMediaUrl` | string | http/https url, up to 255 chars | blank string | no |
| `latitude` | float | latitude | 0.0 | yes |
| `longitude` | float | longitude | 0.0 | yes |
| `startTime` | integer | unsigned integer 64 | 0 | yes |
| `endTime` | integer | unsigned integer 64 | 0 | yes |
| `callbackUrl` | string | http/https url, up to 255 chars | \- | no |
| `ticketId` | string | up to 255 chars | \- | yes, sha256(`ticketId`) |
| `userId` | string | up to 255 chars | \- | no |
| `nftId` | string | valid GETProtocol NFT Id (e.g. POLYGON-123-123) | \- | no |
| `imageUrl` | string | http/https url, up to 255 chars | blank string | no |
| `mediaUrl` | string | http/https url, up to 255 chars | blank string | no |
| `price` | string | valid price string represented | \- | yes |
| `orderTime` | integer | unsigned integer 64 | now unix timestamp | yes |
| `to` | string | blockchain wallet address | \- | yes |
| `metadataAttributes` | json | Opensea metadata attributes standard | \- | yes |
| `metadataTemplateId` | string | uuid | \- | no |
| `name` | string | up to 128 chars | {eventname}-{tokenid} | yes |
| `description` | string | up to 10240 chars | Event Collectible #{tokenId} Issued for {eventname}{shopUrl}) by {intergratorName}. Powered by OPEN TIcketing. | yes |

> 📘
>
> ###
>
> Null vs Empty
>
> On event and tickets updates with `eventUpdate` or `ticketUpdate` actions respectively, you can send the **default value** from the table above on non required fields to have them cleared.
>
> You can also send the `json null` value i.e. `"imageUrl": null` or completely omit fields that are not intended to be updated.

###

Data Field Details

| data field | detail |
| --- | --- |
| `eventId` | Event ID reference, created by the api caller, to indicate how this event is referenced in all stream requests where it is required. For example, if you send a `newEvent` request with the field `eventId="test-event"` , then a `soldTicket` request with the field `eventId="test-event` will mint tickets on that newly created event. This field must be unique per api caller. |
| `eventName` | The name of the event, created by the api caller. This name will be publicly available. |
| `currency` | The main currency used to sell the tickets for this event. All `price` fields sent will be assumed to be in this currency. |
| `shopUrl` | The url for the main shop/page where tickets where sold from. |
| `coverImageUrl` | The main cover image url for the event. E.g. a `.jpg` url |
| `coverMediaUrl` | The main cover media url for the event. E.g. a `youtube.com` or `.mp4` url |
| `defaultNftImageUrl` | The image url to use on all tickets minted for the event, if the ticket itself doesn't specify one. |
| `defaultNftMediaUrl` | The media url to use on all tickets minted for the event, if the ticket itself doesn't specify one. |
| `latitude` | The latitude where the event will take place. |
| `longitude` | The longitude where the event will take place. |
| `startTime` | The unix timestamp of when the event will start. |
| `endTime` | The unix timestamp of when the event will end. |
| `callbackUrl` | The url where GETProtocol should send callbacks to. This url must be publicly reachable without authentication and should return a 200 OK on successful processing of a callback. See [Callbacks](https://docs.onopen.xyz/reference/ticket-engine-api-callbacks) for more detail on the sent callbacks and their data. |
| `ticketId` | Ticket ID reference, created by the api caller, to indicate how this ticket is referenced in all stream requests where it is required. For example, if you send a `soldTicket` request with the field `ticketId="test-ticket"` , then an `invalidateTicket` request with the field `ticketId="test-ticket"` will invalidate the newly created ticket. This field must be unique per api caller. |
| `userId` | User Id reference, created by the api caller, to indicate to which user the ticket refers to. |
| `nftId` | GETProtocol generated NFT Id. This field can be used, as an alternative to `ticketId` , to identify the ticket the request refers to in the case that the api caller doesn't have the `ticketId` available. This field is generated by GETProtocol and is publicly available on the blockchain. |
| `imageUrl` | The main image url for the ticket. E.g. a `.jpg` url. |
| `mediaUrl` | The main media url for the ticket. E.g. a `youtube.com` or `.mp4` url. |
| `price` | The price the ticket was sold for. |
| `orderTime` | The unix timestamp of when the ticket was sold. |
| `to` | The user owned custom wallet address. This field should only be used whenever the api caller knows the wallet address of the user the ticket was sold or resold to. In case the api caller wants to let the tickets be minted to a new user wallet, this field should not be sent. |
| `metadataAttributes` | Additional metadata attributes of the ticket. For more details on how these metadata attributes should be constructed for proper display in OpenSea, please check [this](https://docs.opensea.io/docs/metadata-standards#attributes) page. |
| `metadataTemplateId` | The id for a metadate template created within the NFT studio. Attributes specified within metadataAttributes will override attributes generated from a specified template |
| `name` | The name of the ticket, created by the api caller. This name will be publicly available. |
| `description` | The description of the event, created by the api caller. This name will be publicly available |


Next you can find an example payload for an event with a single ticket that went through all the possible states until being claimed by/to a ticket buyer account:

Example Request Payload

```
[
{
"action": "newEvent",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"eventName": "porro ut autem",
"currency": "EUR",
"shopUrl": "http://roberto.net",
"coverImageUrl": "https://placeimg.com/640/480/nature",
"coverMediaUrl": "",
"defaultNftImageUrl": "https://assets.onopen.xyz/open-default-collectible-image.png",
"defaultNftMediaUrl": "https://www.youtube.com/watch?v=cjXSeElvbss",
"startTime": 1652285087,
"endTime": 1652285087,
"latitude": -24.2066,
"longitude": -159.3224,
"callbackUrl": "http://callback.url/callback"
}
},
{
"action": "soldTicket",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"ticketId": "10cd5d96-ecc1-43ae-b1bc-b248da171c92",
"userId": "48d68f38-1376-4eb4-96a3-6bd65efce492",
"name": "ticket abc",
"description": "the description for ticket abc",
"price": "136.91",
"imageUrl": "http://placeimg.com/640/480",
"mediaUrl": "https://www.youtube.com/watch?v=cjXSeElvbss",
"metadataAttributes": "[{\"trait_type\":\"Ticket Type\", \"value\":\"Early bird\"},{\"display_type\":\"boost_number\", \"trait_type\":\"Ticket power\", \"value\":\"3\"}]"
}
},
{
"action": "soldTicket",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"ticketId": "719cf724-75c0-4fb4-ba4e-2f6cd67a328e",
"price": "15.00"
}
},
{
"action": "soldTicket",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"ticketId": "4c5bb3f1-d281-4774-a08a-b34813126f03",
"price": "10.00"
}
},
{
"action": "updateTicket",
"data": {
"ticketId": "10cd5d96-ecc1-43ae-b1bc-b248da171c92",
"name": "ticket abc",
"description": "the description for ticket abc",
"imageUrl": "http://updated.image.com/",
"mediaUrl": "http://updated.video.com/",
"metadataAttributes": "[{\"trait_type\":\"Ticket Type\", \"value\":\"Early bird\"},{\"display_type\":\"boost_number\", \"trait_type\":\"Ticket power\", \"value\":\"4\"}]"
}
},
{
"action": "resoldTicket",
"data": {
"nftId": "POLYGON-123-123",
"userId": "54c28708-9406-4bc6-b609-bee17e051173",
"price": "466.25"
}
},
{
"action": "scannedTicket",
"data": {
"ticketId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
}
},
{
"action": "updateEvent",
"data": {
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"imageUrl": "https://placeimg.com/640/480/tech",
"defaultNftImageUrl": "https://assets.onopen.xyz/open-default-collectible-image.png"
}
},
{
"action": "checkedInTicket",
"data": {
"nftId": "POLYGON-123-123",
}
},
{
"action": "claimedTicket",
"data": {
"ticketId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"to": "0x72e5c6e078001644b15c3b8d56a019c8f551adc4"
}
},
{
"action": "claimedTicket",
"data": {
"ticketId": "719cf724-75c0-4fb4-ba4e-2f6cd67a328e",
"userId": "138b694b-7d77-4117-a337-4c11f0723573"
}
},
{
"action": "claimedTicket",
"data": {
"ticketId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"userId": "25685833-604d-4b98-9f25-067aed6912fe",
"to": "0x3d712EE26e407DC383a451466B7a93a42094dBA1"
}
}
]
```

> 📘
>
> ###
>
> Limits & Ordering
>
> Each request can include up to 5000 actions. Actions are processed and their result returned in the order they are sent in the request.

A request with the previous payload should yield a response similar to:

Example Response Payload

```
{
"status": "success",
"data": [
{
"status": "success",
"action": "newEvent",
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"actionPromise": "a58b6a0c-2e59-4bb0-8b19-9a3f77c934b3"
},
{
"status": "success",
"action": "soldTicket",
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"ticketId": "10cd5d96-ecc1-43ae-b1bc-b248da171c92",
"actionPromise": "22709bf7-59a8-4751-82f1-06184b9dcf22"
},
{
"status": "success",
"action": "updateTicket",
"ticketId": "10cd5d96-ecc1-43ae-b1bc-b248da171c92",
"actionPromise": "3280fc95-d8fa-4b77-a375-9216f27f1df3"
},
{
"status": "success",
"action": "resoldTicket",
"nftId": "POLYGON-123-123",
"actionPromise": "d31dc1c8-641c-4c3b-a2d1-78963f9c8590"
},
{
"status": "success",
"action": "scannedTicket",
"ticketId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"actionPromise": "c9d73b07-8a85-4198-af4d-f6e3fd7a4b8f"
},
{
"status": "success",
"action": "updateEvent",
"eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"actionPromise": "a487b584-03a9-45fc-995e-badb42250c25"
},
{
"status": "success",
"action": "checkedInTicket",
"nftId": "POLYGON-123-123",
"actionPromise": "c545e395-e13e-4969-9b50-52c14ed782f6"
},
{
"status": "success",
"action": "claimedTicket",
"ticketId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
"actionPromise": "c2e8df23-6411-46e0-8ec2-61cb0a29f6af"
}
]
}
```

> 👍
>
> ###
>
> Save the promise
>
> Each successful action request will return you an `actionPromise`. Save it on your data model such that you can use it later to query for each action request status.

CURL request:
```bash
curl --request POST \
     --url https://engine.play.onopen.xyz/stream \
     --header 'accept: application/json' \
     --header 'content-type: application/json'
```

responses examples:

200 - success
```json
{
  "status": "success",
  "data": [
    {
      "status": "success",
      "action": "newEvent",
      "eventId": "d240f841-11c3-4140-b7d4-d18c87954ffe",
      "actionPromise": "17b29b21-10bd-44dc-8c05-f6bb63ff6efc"
    }
  ]
}
```

200 - multi
```json
{
  "status": "multi",
  "data": [
    {
      "status": "success",
      "action": "newEvent",
      "eventId": "d634e8db-be4c-43db-82cb-384d22692701",
      "actionPromise": "c08f35f7-b566-46ff-b92f-537efde00f37"
    },
    {
      "status": "error",
      "errors": [
        {
          "param": "currency",
          "message": "is a required field"
        }
      ],
      "action": "newEvent",
      "eventId": "d634e8db-be4c-43db-82cb-384d22692701",
      "requestData": {
        "eventId": "d634e8db-be4c-43db-82cb-384d22692701",
        "eventName": "iusto minima iure",
        "currency": "",
        "shopUrl": "http://shop.url",
        "coverImageUrl": "http://placeimg.com/640/480",
        "coverVideoUrl": "https://www.youtube.com/watch?v=cjXSeElvbss",
        "defaultNftImageUrl": "https://images.get-blockchain.io/get-protocol-default.png",
        "defaultNftVideoUrl": "https://www.youtube.com/watch?v=cjXSeElvbss",
        "startTime": 1663062631,
        "endTime": 1663062631,
        "latitude": 49.3256,
        "longitude": 47.9646,
        "callbackUrl": "http://callback.url/callback"
      }
    }
  ]
}
```

400 - error
```json
{
  "status": "error",
  "error": "all_actions_invalid",
  "message": "The requested actions are all invalid",
  "data": [
    {
      "status": "error",
      "errors": [
        {
          "param": "action",
          "message": "must not be empty"
        }
      ],
      "requestData": {
        "action": "",
        "data": {
          "callbackUrl": "http://callback.url/callback",
          "currency": "USD",
          "eventId": "853b3547-fbdc-4ee4-950f-532db74bff01",
          "eventName": "in tempora natus",
          "coverImageUrl": "http://placeimg.com/640/480",
          "coverVideoUrl": "https://www.youtube.com/watch?v=cjXSeElvbss",
          "defaultNftImageUrl": "https://images.get-blockchain.io/get-protocol-default.png",
          "defautlNftVideoUrl": "https://www.youtube.com/watch?v=cjXSeElvbss",
          "latitude": 82.0601,
          "longitude": 37.5888,
          "shopUrl": "https://shop.url",
          "endTime": 1663062509,
          "startTime": 1663062509
        }
      }
    }
  ]
}
```

<!-- Source file: ./apis/Ticket Engine API V2/f-ticket-engine-api-actions.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Actions

```
GET https://engine.play.onopen.xyz/actions/{promise}
```

Description: Upon successful event/ticket action creation through the Stream endpoint, an actionPromise will be issued and returned. Use it to query it's status:
statusdescriptionwaiting_broadcastAction is still waiting in queue to get broadcast on chainwaiting_fundsAction is waiting on an integrator fuel top up…

Upon successful event/ticket action creation through the Stream endpoint, an `actionPromise` will be issued and returned. Use it to query it's status:

| status | description |
| --- | --- |
| `waiting_broadcast` | Action is still waiting in queue to get broadcast on chain |
| `waiting_funds` | Action is waiting on an integrator fuel top up |
| `pending` | Action was broadcast and is waiting confirmation |
| `confirmed` | Action was broadcast and successfully confirmed |
| `error` | Action was broadcast on chain but an error occurred |
| `wont_broadcast` | Action was invalid (e.g. selling ticket on non existent event) and a broadcast on chain won't be attempted |
| `no_broadcast_required` | Some actions might not need a broadcast on chain-at all e.g. `updateTicket` |


CURL request:
```bash
curl --request GET \
     --url https://engine.play.onopen.xyz/actions/d240f841-11c3-4140-b7d4-d18c87954ffe \
     --header 'accept: application/json'
```

responses examples:


200 - Confirmed
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "userId": "105ec71a-c740-478e-88ec-9804b4fd1d9f",
  "status": "confirmed",
  "blockchainHumanId": "amoy",
  "eventIndex": 3621,
  "tokenId": 1,
  "nftId": "AMOY-3621-1",
  "eventAddress": "0x38fb127222696AEa961EB29C323A2681fB0D9B2F",
  "txHash": "0x23d3ba97ce8aabd87fa4341300d02d2f8c99454f0bbcdc3bc0d0fd750b003b3f",
  "userWallet": "0x718d8c00E26671e99e0B0d23f6A1e0EDD43436ca",
  "userWalletTicketUrl": "https://wallet.dev.onopen.xyz/user/7b60720d-eecd-4cf5-bdd9-44390de646df/amoy/12707/1",
  "explorerUrl": "https://explore.dev.onopen.xyz/ticket/amoy-3621-1",
  "callbacks": [
    {
      "type": "soldTicket",
      "data": {
        "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e"
      }
    },
    {
      "type": "userCreated",
      "data": {
        "userId": "105ec71a-c740-478e-88ec-9804b4fd1d9f",
        "userUuid": "7b60720d-eecd-4cf5-bdd9-44390de646df"
      }
    }
  ]
}
```


200 - Won't Broadcast
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "wont_broadcast",
  "error": "event_not_found",
  "message": "The event was not yet created"
}
```


200 - Waiting Broadcast
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "waiting_broadcast",
  "eventAddress": "0x315A759CA7E3029468e63B011147933Ef11910aD"
}
```


200 - Pending
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "waiting_broadcast"
}
```


200 - Broadcast Error
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "error"
}
```

200 - No Broadcast Required
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "updateTicket",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "no_broadcast_required",
  "nftId": "POLYGON-4-11",
  "eventAddress": "0x315A759CA7E3029468e63B011147933Ef11910aD",
  "explorerUrl": "https://playground.explorer.get-protocol.io/ticket/polygon-4-11"
}
```

200 - User Already Owns
```json
{
  "promise": "1bd35118-1048-4432-8cde-62b3fd1d3606",
  "action": "resoldTicket",
  "ticketId": "dab79f9e-48a3-402e-9cb6-57e8db51701c",
  "status": "no_broadcast_required",
  "nftId": "POLYGON-4-11",
  "eventAddress": "0x315A759CA7E3029468e63B011147933Ef11910aD",
  "explorerUrl": "https://playground.explorer.get-protocol.io/ticket/polygon-4-11",
  "error": "user_already_owns",
  "message": "The user already owns this ticket"
}
```

200 - Waiting Funds
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "waiting_funds"
}
```

200 - Waiting Funds
```json
{
  "promise": "d240f841-11c3-4140-b7d4-d18c87954ffe",
  "action": "soldTicket",
  "eventId": "1b15b541-7d60-4ae8-b41f-aca6b981a6e7",
  "ticketId": "9823826e-52c4-4e30-9372-1394d6c9df5e",
  "status": "waiting_funds"
}
```

<!-- Source file: ./apis/Ticket Engine API V2/g-ticket-engine-api-callbacks.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Callbacks

```
POST https://webhook.site/
```

Description: Upon successful event/ticket action registration on the blockchain, a callback request (or multiple, depending on the action) will be issued to the URL given as callbackUrl at the time of event creation through the Stream step.
Due to the nature of blockchain, the process of writing transaction onto…

Upon successful event/ticket action registration on the blockchain, a callback request (or multiple, depending on the action) will be issued to the URL given as `callbackUrl` at the time of event creation through the Stream step.

Due to the nature of blockchain, the process of writing transaction onto chain can sometimes be difficult to predict and because of that we treat it as an asynchronous process. By offering a webhook endpoint from within your own platform it makes it easy to receive updates on which promises are ready to be checked after an update (be it an error or a success processing on the blockchain) and which blockchain addresses have been created or added alongside the users in the Stream requests.

The `callbackUrl` must respond to secured communication over HTTPS.

The callback is considered successful if a 200 OK or 201 CREATED is returned. In any other case, the callback server will retry to deliver the message following an exponential backoff with up to 5 attempts.

The callbacks only contain ids to your records. This intentional. The callback will never contain any sensitive data. Secondly callbacks like these are susceptible to spoofing and replay attacks. Therefore you should retrieve the data yourself using the api.

Body Params
callbackType
string
required
The type of the callback being sent. Possible types are validationError, blockchainStatusUpdate, userCreated and userUpdated

promise
string
required
Defaults to d240f841-11c3-4140-b7d4-d18c87954ffe
Promise that just got updated, and ready to be checked with GET /action endpoint

d240f841-11c3-4140-b7d4-d18c87954ffe
userId
string
User ID to which the callback refers to. Only available on userCreated and userUpdated callback types

Headers
Content-Type
string
Defaults to application/json
application/json

CURL request:
```bash
curl --request POST \
     --url https://webhook.site/ \
     --header 'Content-Type: application/json' \
     --header 'accept: application/json' \
     --data '{"promise": "d240f841-11c3-4140-b7d4-d18c87954ffe"}'
```

<!-- Source file: ./apis/Ticket Engine API V2/h-ticket-engine-api-metadata.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Metadata

```
GET https://engine.play.onopen.xyz/metadata/{blockchainHumanId}/{eventIndex}/{tokenID}
```

Description: This endpoint returns all the relevant metadata for a specific NFT.
This endpoint will always return an image in the following order:

uri sent on the soldTicket or updateTicket (whichever is the latest) Stream request for the NFT, if not empty
defaultNftImageUrl sent on the newEvent or updateEvent …

This endpoint returns all the relevant metadata for a specific NFT.

This endpoint will always return an `image` in the following order:

*   `uri` sent on the `soldTicket` or `updateTicket` (whichever is the latest) Stream request for the NFT, if not empty
*   `defaultNftImageUrl` sent on the `newEvent` or `updateEvent` (whichever is the latest) Stream request for the NFT, if not empty
*   fallback OPEN TIcketing image url (https://assets.onopen.xyz/open-default-collectible-image.png) if both of the above are empty

blockchainHumanId
string
required
Defaults to polygon

eventIndex
int32
required
Defaults to 1

tokenID
int32
required
Defaults to 1

CURL request
```bash
curl --request GET \
     --url https://engine.play.onopen.xyz/metadata/polygon/1/1 \
     --header 'accept: application/json'
```

responses:

200 - Result
```json
{
  "description": "Shop: http://alan.info",
  "external_url": "http://example.com/ticket/polygon-1-1",
  "image": "https://images.get-blockchain.io/get-protocol-default-nftimage.png",
  "animation_url": "https://www.youtube.com/watch?v=cjXSeElvbss",
  "youtube_url": "https://www.youtube.com/watch?v=cjXSeElvbss",
  "name": "iure debitis voluptate #1",
  "attributes": [
    {
      "display_type": "date",
      "trait_type": "Event Starts",
      "value": 1652709891
    },
    {
      "display_type": "date",
      "trait_type": "Event Ends",
      "value": 1652709891
    }
  ]
}
```

400 - Bad Request
```json
{}
```

404 - Not Found
```json
{}
```

<!-- Source file: ./apis/Ticket Engine API V2/i-user.md -->

---
### ⚡️ ==================== ⚡️
---

Title: User (with userID)

```
GET https://engine.play.onopen.xyz/user/id/{userId}
```

Description: This endpoint returns all the relevant data for a specific user, including:

The user's wallets, including the tickets they contain.
The tickets inside custom wallets registered to the user.

The following example shows a payload returned by this endpoint:
{
"status": "ok",
"data": {
…

This endpoint returns all the relevant data for a specific user, including:

*   The user's wallets, including the tickets they contain.
*   The tickets inside custom wallets registered to the user.

The following example shows a payload returned by this endpoint:

```
{
"status": "ok",
"data": {
"userId": "user-abc",
"userUuid": "affbab56-2dad-4fcf-82c8-e7450c57a0d4",
"userWallets": [
{
"address": "0xF8fcB0F4Caec2d7448c2bb579122d246f31A934D",
"tickets": [
{
"id": "POLYGON-1-1",
"blockchainHumanId": "POLYGON",
"eventIndex": 1,
"tokenId": 1,
"eventContract": "0x6afa4c6d3c8c8c860f7bcc13c9f9cb2721cc09b8"
},
{
"id": "POLYHON-3-3",
"blockchainHumanId": "POLYGON",
"eventIndex": 3,
"tokenId": 3,
"eventContract": "0x5BFA4c6d3C8c8c860F7BcC13C9f9CB2721cC09b8"
}
]
}
],
"customWalletTickets": [
{
"id": "POLYGON-3-5",
"blockchainHumanId": "POLYGON",
"eventIndex": 3,
"tokenId": 2,
"eventContract": "0x5BFA4c6d3C8c8c860F7BcC13C9f9CB2721cC09b8",
"initialAddress": "0x21ca65b9c3A943b172EedaC10501Eca483A1Ed00"
}
]
}
}
```

The returned payload will contain the following fields:

| key | description |
| --- | --- |
| status | Always `ok`, this might change in the future |
| data | data block (see below) |

**Data block**

| key | description |
| --- | --- |
| userId | The user ID |
| userUuid | The user Uuid (Only available when the user has an user wallet) |
| userWallets | Array of user wallet blocks (see below) |
| customWalletTickets | Array of ticket blocks (see below) that were initially sold to the queried user. |

**User wallet block**

| key | description |
| --- | --- |
| address | The blockchain address of the wallet |
| tickets | Array of tickets blocks (see below) located in the wallet |

**Ticket block**

| key | description |
| --- | --- |
| id | The NFT ID of the ticket |
| blockchainHumanId | The human ID of the blockchain on which the ticket is located |
| eventIndex | The event index of the ticket |
| tokenId | The token ID of the ticket |
| eventContract | The blockchain address of the tickets event |
| initialAddress | The initial address where the ticket was sent. The user might have moved the ticket to a different address after the event completed, this isn't tracked by this endpoint. |

Path Params:
userId
string
required

Query Params:
blockchainHumanId
string
Defaults to polygon
Filter the result on blockchain human ID (Only valid in combination with eventIndex)

eventIndex
string
Filter the result on eventIndex (Only valid in combination with blockchainHumanId)

CURL request:
```bash
curl --request GET \
     --url 'https://engine.play.onopen.xyz/user/id/userId?blockchainHumanId=polygon' \
     --header 'accept: application/json'
```

responses:

200 - Result
```json
{}
```

400 - Result
```json
{}
```

<!-- Source file: ./apis/Ticket Engine API V2/j-user-with-userid-copy.md -->

---
### ⚡️ ==================== ⚡️
---

Title: User (with userUuid)

```
GET https://engine.play.onopen.xyz/user/uuid/{userUuid}
```

Description: This endpoint returns all the relevant data for a specific user, including:

The user's wallets, including the tickets they contain.
The tickets inside custom wallets registered to the user.

The following example shows a payload returned by this endpoint:
{
"status": "ok",
"data": {
…

This endpoint returns all the relevant data for a specific user, including:

*   The user's wallets, including the tickets they contain.
*   The tickets inside custom wallets registered to the user.

The following example shows a payload returned by this endpoint:

```
{
"status": "ok",
"data": {
"userUuid": "affbab56-2dad-4fcf-82c8-e7450c57a0d4",
"userWallets": [
{
"address": "0xF8fcB0F4Caec2d7448c2bb579122d246f31A934D",
"tickets": [
{
"id": "POLYGON-1-1",
"blockchainHumanId": "POLYGON",
"eventIndex": 1,
"tokenId": 1,
"eventContract": "0x6afa4c6d3c8c8c860f7bcc13c9f9cb2721cc09b8"
},
{
"id": "POLYGON-3-3",
"blockchainHumanId": "POLYGON",
"eventIndex": 3,
"tokenId": 3,
"eventContract": "0x5BFA4c6d3C8c8c860F7BcC13C9f9CB2721cC09b8"
}
]
}
]
}
}
```

The returned payload will contain the following fields:

| key | description |
| --- | --- |
| status | Always `ok`, this might change in the future |
| data | data block (see below) |

**Data block**

| key | description |
| --- | --- |
| userUuid | The user Uuid |
| userWallets | Array of user wallet blocks (see below) |
| customWalletTickets | Array of ticket blocks (see below) that were initially sold to the queried user. |

**User wallet block**

| key | description |
| --- | --- |
| address | The blockchain address of the wallet |
| tickets | Array of tickets blocks (see below) located in the wallet |

**Ticket block**

| key | description |
| --- | --- |
| id | The NFT ID of the ticket |
| blockchainHumanId | The human ID of the blockchain on which the ticket is located |
| eventIndex | The event index of the ticket |
| tokenId | The token ID of the ticket |
| eventContract | The blockchain address of the tickets event |
| initialAddress | The initial address where the ticket was sent. The user might have moved the ticket to a different address after the event completed, this isn't tracked by this endpoint. |

Path Params:
userUuid
string
required

Query Params:
blockchainHumanId
string
Defaults to polygon
Filter the result on blockchain human ID (Only valid in combination with eventIndex)

eventIndex
string
Filter the result on eventIndex (Only valid in combination with blockchainHumanId)


CURL request:
```bash
curl --request GET \
     --url 'https://engine.play.onopen.xyz/user/uuid/userUuid?blockchainHumanId=polygon' \
     --header 'accept: application/json'
```

responses:

200 - Result
```json
{}
```

400 - Result
```json
{}
```

<!-- Source file: ./apis/Ticket Engine API V2/k-wallet-generate-jwt.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Wallet Generate JWT

```
GET https://engine.play.onopen.xyz/wallet/generate_token
```

Description: This endpoint allows integrators to request a valid JWT that is required by the wallet/sign endpoint. The JWT is requested from this endpoint using the API Key provided to the integrators. The token is valid for 15 minutes and can only be used once.
Signature Key
The tokens are signed with a symmetr…

This endpoint allows integrators to request a valid JWT that is required by the `wallet/sign` endpoint. The JWT is requested from this endpoint using the API Key provided to the integrators. The token is valid for 15 minutes and can only be used once.

Signature Key

-----------------

The tokens are signed with a symmetrical key using HMAC256. This key can be shared upon contacting us if you would like to generate your JWTs.

JWT Payload

---------------

json

```
{
"id": "1",            //id of the user
"exp": 1712873700,    //expiration time of the jwt
"jti": "testjti",     //jti to prevent replay attacks
"id_type": "userId",  //type of the id to identify the user. could be userId, userUuid or address
"version": 1,         //version of the endpoint
"iss": "artemis",     //integrator the jwt belongs to
"iat": 1712872800     //issued at
}
```

| Field | Description |
| --- | --- |
| id | user id, the value must relate to an existing user |
| id\_type | type of id for the user id. values could be one of `userId`, `userUuid`, `address`. |
| iat | issued at time in Unix timestamp seconds |
| exp | expiration time in Unix timestamp seconds, should be iat + 15 minutes. |
| iss | integrator slug |
| jti | unique id for JWT to prevent replay attacks. also valid for 15 minutes |
| version | version of the API endpoint |

Errors

----------

Here are potential errors you might encounter:

| HTTP Status Code 400 |
| --- |
| 'id' must not be empty |
| 'id\_type' must not be empty |
| id\_type must be one of: userId, userUuid, address |

| HTTP Status Code 401 |
| --- |
| apikey is invalid |

| HTTP Status Code 500 |
| --- |
| internal server error |

Path Params
id
string
required
the userId, userUuid or blockchain address of the user

idType
string
required
corresponding id type of the provided id "userId", "userUuid" or "address".

CURL request:
```bash
curl --location --request POST 'https://api.playground.engine.get-blockchain.io/wallet/generate_token?id=d2d03d41-a53b-40d5-b606-f7ee11f3bf5c&idType=userId' \
--header 'X-Api-Key: <API-KEY>' \
```

responses:

200 - Result
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuZHQiLCJleHAiOjE3MTkyMjkxNDAsImlhdCI6MTcxOTIyODI0MCwianRpIjoiZjY1ZmEyOGEtZGY5Yy00M2NhLThkY2ItZjlmZGIxNmExZTg2IiwiaWQiOiJjYzU3YzhmZi03ZjgzLTRlNjUtOGU1MC0yYjcwY2QyNWYwMGQiLCJpZF90eXBlIjoidXNlclV1aWQiLCJ2ZXJzaW9uIjoxfQ.761P_IRhX2KroNiis5JBqOezQD3Lvj4cV7MpUrkhH1g"
}
```

400 - Result
```json
{}
```

<!-- Source file: ./apis/Ticket Engine API V2/l-wallet.md -->

---
### ⚡️ ==================== ⚡️
---

Title: Wallet Sign

```
POST https://engine.play.onopen.xyz/wallet/sign
```

Description: This endpoint enables signing messages with custodial wallets that is used to SIWE.

Authentication

------------------

The `wallet/sign` endpoint works with a Bearer Token provided in the authentication header. The string provided as the token is a JWT with the following fields:

JSON

```
{
"id": "1",            //id of the user
"exp": 1712873700,    //expiration time of the jwt
"jti": "testjti",     //jti to prevent replay attacks
"id_type": "userId",  //type of the id to identify the user. could be userId, userUuid or address
"version": 1,         //version of the endpoint
"iss": "artemis",     //integrator the jwt belongs to
"iat": 1712872800     //issued at
}
```

The JWTs are specific for the user and must be generated for different users. To obtain a JWT for a user, it is possible to send a request to `wallet/generate_token`. This is discussed in `Wallet Generate JWT` section. To be able to create JWTs without sending a request to `wallet/generate_token`, the payload of the JWT must be complete and valid, the JWT must be signed with HMAC256 and the signature key must be valid. The signature key will be provided to integrators upon request.

| JWT Payload Field | Description |
| --- | --- |
| id | user id, the value must relate to an existing user |
| id\_type | type of id for the user id. values could be one of `userId`, `userUuid`, `address`. |
| iat | issued at time in Unix timestamp seconds |
| exp | expiration time in Unix timestamp seconds, should be iat + 15 minutes. |
| iss | integrator slug |
| jti | unique id for JWT to prevent replay attacks. also valid for 15 minutes |
| version | version of the API endpoint |

Message

-----------

The endpoint is made to sign a message with the user's wallet. The provided message is processed and returned as a signature that could be used to Sign in with Ethereum (SIWE). The message `hello world` was signed for an arbitrary user, which produced the following result: `{     "signature": "0xd80dac506b0045a8727507910cc3038fae4328595fa3e0ecca2cf0c4c75b8f911bcd778086d0cae70b400da77496bee87b3af7ebaf55dee055c4f75c26ce3cbd1c" }`

Body Params
message
string
The message to be signed for the user

Headers
Authorization
string
required
JWT Bearer token retrieved with /wallet/generate_token or generated by your backend using the pre shared key

CURL request:
```bash
curl --location 'https://api.playground.engine.get-blockchain.io/wallet/sign/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <JWT>' \
--data '{
    "message":"hello world"
}'
```

responses:

200 - Result
```json
{
  "signature": "0xd80dac506b0045a8727507910cc3038fae4328595fa3e0ecca2cf0c4c75b8f911bcd778086d0cae70b400da77496bee87b3af7ebaf55dee055c4f75c26ce3cbd1c"
}
```

400 - Result
```json
{
    "error": <REASON>
}
```

401 - Result
```json
{
    "error": <REASON>
}
```

500 - Result
```json
{
    "error": <REASON>
}
```
