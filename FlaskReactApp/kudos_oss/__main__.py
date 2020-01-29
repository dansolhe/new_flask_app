from __future__ import absolute_import, print_function

# For the authenticated user, fetches all favorited github open source projects
GET /kudos

# Favorite a github open source project for the authenticated user
POST /kudos

# Unfavorite a favorited github open source project
DELETE /kudos/:id
