from django.forms import ModelForm, ValidationError

from .models import Product, Bid, Remark

def valid_bid(amount_, id):
    item = Product.objects.get(pk=id)
    if item.bids.all.count == 0:
        if int(amount_) > item.startBid:
            return True
    if int(amount_) > item.bids.first.amount:
        return True

    return False

class NewProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "desc", "startBid", "img", "category"]
        labels = {
            'title': ('Product Name'),
            'desc': ('Product Description'),
            'startBid': ('Starting Bid ($)'),
            'img': ('Image (URL)'),
            'category': ('Category'),
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        labels = {
            "amount" : ('Enter Bid'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Remark
        fields = ["message"]
        labels = {
            "message": ('Post Comment: '),
        }
