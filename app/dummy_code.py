
my_posts = [
  { "title": "title of post 1", "content": "content of post 1", "id": 1 },
  { "title": "favorite foods", "content": "I like pizza", "id": 2 },
]

def find_post(id):
  for post in my_posts:
    if post["id"] == id:
      return post

def find_index_of_post(id):
  for idx, post in enumerate(my_posts):
    if post["id"] == id:
      return idx


# Reference
# def create_post(payload: dict = Body(...)):

# @app.get('/posts/{id}/{string}/{decimal}')
# def get_post(id, string, decimal):
#   print(id)
#   print(string)
#   print(decimal)
#   return {
#     "post_details": f"Here is post {id}",
#     "params": [id, string, decimal]
#   }

# def get_post(id: int, response: Response):
# response.status_code = status.HTTP_404_NOT_FOUND
# return { 'message': f"Post with id: {id} doesn't exists"}