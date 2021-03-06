# Foodie Reviews
Foodie Reviews is a django application that lets its users express their love and passion for food together.

###
* Sign up and create an account
* Navigate to "add a new review" at the top of the page
* Write your review and click update
* Congrats! You wrote your first restaurant review!
* Click the "Reviews" button at the top of the page to navigate to all reviews

## Screenshots

### User's Reviews
![User](main_app/static/img/Userreviews.png)

### All Reviews
![Reviews](main_app/static/img/Allreviews.png)

### Future Considerations
* Give users an option to add images to their food reviews
* Give a search option for reviews by Restaurant name

### Code Snippets

``` python
# Creation and Update of Reviews
class PostCreate(CreateView):
  model = Post
  fields = ['name', 'location', 'review', 'rating']
  success_url = '/posts'
  
  def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.user = self.request.user
      self.object.save()
      return HttpResponseRedirect('/posts/' + str(self.object.pk))

class PostUpdate(UpdateView):
  model = Post
  fields = ['name', 'location', 'review', 'rating']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/posts/')

```
