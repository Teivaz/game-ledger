# Game Ledger
Tracking board games progress

## API

### Access levels
0 – internal, can never be accessed through API.
1 – reserved, do not use.
2 – private, can only be accessed by the owner of the resource.
3 – party, can be accessed by the members of the same party.
4 – users, can be accessed by all users.
5 – public, can be accessed by everyone.

### Resources

1. `User`
- `id` – unique identifier of the user. Read access level (AL) 4, write AL 0.
- `email` – unique email used for authentication. Read and write AL 2.
- `name` – displayed user name. Read AL 4, write AL 2.
- `profile_image` – avatar. Read AL 4, write AL 2.
- `parties` – list of `Party.id` that the user is member of. Read AL 2, write AL 0.
- `owned_games` – list of `Game.id` that the user is the owner of. Read AL 3, write AL 2.

2. `Game`. All fields have read AL 5, 3, or 2 (depending on value of the `access level` field) and write AL 2 unless specified.
- `id` – unique identifier of the game. Write AL 0.
- `name` – displayed name of the game.
- `revision` – a text field, revision of the game.
- `rules` – a text field containing game rules.
- `profile_image`
- `images` – other photos of the game, e.g. rules, box.
- `custom_fields` – a list of string with names describing fields apart from the score that the game has.
- `author` – `User.id` of the author of the resource. Write AL 0.
- `access_level` – (public, party, private). Note: in the future users should not be allowed to set the public level.

3. `Party`. All fields have read and write AL 3 unless specified. Note: all members are considered to be owners of resource.
- `id` – unique party identifier. Write AL 0.
- `name` – the displayed name of the party.
- `profile_image`
- `members` – list of `User.id`
- `games` – list of `Game.id`
- `game_sessions` – list of `GameSession.id`

4. `GameSession`. All fields have read and write AL 3 unless specified.
- `id` – unique game session identifier. Write AL 0.
- `game` – the `Game.id` that was played.
- `session_date` – date and time of the played session.
- `session_duration`
- `party` – the `Party.id` that this session belongs to.
- `participants` – the list of `User.id` that participated in this session.
- `scores` – the dictionary of `{User.id: number}` where higher number means better overall score.
- `custom_fields` – the dictionary of `{Game.custom_field: {User.id: number}}`

5. `Data`. Represents any image file. All fields have read AL 4 (Note: not very secure, should follow the same procedure as `Game` resource) and write AL 0.
- `id` – a unique identifier of the resource.
- `type` – a MIME type of the image.
- `content` – the binary content of the image.
- `owner` – the `User.id`.

### API details
Following names are directly linked to the eponymous resource and are URL paths for the HTTP API endpoint with corresponding methods.
1. `user`
1.1 `POST` - Access Level (AL) 5. Accepts JSON encoded body with all fields of the resource `User`. Field `email` is required, field `id` is ignored. Upon success returns the identifier of the user and emails activation link. If the field `name` is not provided it should be filled automatically with a simple funny name.
1.2 `GET` – AL 4. Has parameter `id`. Returns json object with all fields that have equal or lower access level. Unregistered users get response 401. Users that share a party also get the field `games`. Owner of the account additionally get the field `email`.
1.3 `PATCH` – AL 2. Requires parameter `id`. Contains JSON encoded body with the fragments of the `User` resource. If the fragment provides the field `id` it needs to match the URL parameter `id`, otherwise it should fail with error 400. Used for modifying the parts of the resource.

2. `user/activate` is not a resource, just a part of authentication mechanism.
2.1 `GET` – AL 5. Requires parameters `token`, and `redirect`. Upon successfull activation invalidates token, sets authentication cookie and redirects to the url specified in the corresponding field.

3. `game` 
3.1 `POST` – AL 4. Accepts JSON encoded body with all fields of the resource `Game`. Fields with insufficient permissions errors are ignored. Upon success creates a resource `Game` and returns its id. The requesting user is set as the author. The created resource id is added the list of `User.owned_games`.
3.2 `GET` – AL 5, 3, or 2 depending on the value of the `access level` field.
 - Requires at least one parameter `id`. Returns JSON encoded list of `Game` resources that can have corresponding access level.
 - Alternatively can require parameters `find`. Returns JSON encoded list of `Game` resources that have corresponding access level and have requested substring in the `Game.name` field.
3.3 `PATCH` – AL 3 or 2 depending on the value of the `access level` field. If the resource specifies AL 5 this method still requires AL 3, otherwise it would fail with 403. Requires parameter `id`. Used for modifying the parts of the resource.

4. `party`
4.1 `POST` – AL 4. Accepts JSON encoded body with all fields of the resource `Party`. Fields with insufficient permissions errors are ignored. Upon success creates a resource `Party`, adds requesting user as a member and returns its id.
4.2 `GET`
 4.2.a Requires at least one parameter `id`. AL 3. Returns JSON encoded list of `Party` resources.
 4.2.b Requries parameter `token`. AL 4. If the token is active it will modify the resource it is associated with by adding the current user id to the list of members.
4.3 `PATCH` – AL 3 or 2 depending on the value of the `access level` field. If the resource specifies AL 5 this method still requires AL 3, otherwise it would fail with 403. Requires parameter `id`. Used for modifying the parts of the resource.

5. `party/invite` – is not a resource, just a part of party management mechanism.
5.1 `GET` – AL 3. Requires parameter `id`. Returns a token that can be used once to join the party with 4.2.b method.

6. `game_session`
6.1 `POST` – AL 3. Requires parameter `party_id`. Accepts JSON encoded body with all fields of the resource `GameSession`. Fields with insufficient permissions errors are ignored. Upon success creates a resource `GameSession`, adds this reource to the `Party.game_sessions` if the users is member of the party.
6.2 `GET` - AL 3. Requires parameter `id`. Returns JSON encoded list of `GameSessions` resources.
6.3 `PATCH` - AL 3. Requires parameter `id`. Used for modifying the parts of the resource.

7. `data`
7.1 `POST` - AL 4. Requires header `Content-Type` with the MIME type of the data being stored. Upon success the user is set as an owner of the created resource.
7.2 `GET` – AL 4. Requires single parameter `id` of the requested resource. The response contains header `Content-Type`, `Content-Length` and the binary body containing the data from the `content` field.
