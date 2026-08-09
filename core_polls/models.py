from django .db import models 


class Poll (models .Model ):
    title =models .CharField (max_length =255 )
    description =models .TextField (blank =True )
    creator =models .ForeignKey ("core_profile.Profile",on_delete =models .CASCADE ,related_name ='polls')
    created_at =models .DateTimeField (auto_now_add =True )

    def __str__ (self ):
        return self .title 


class PollOption (models .Model ):
    poll =models .ForeignKey (Poll ,on_delete =models .CASCADE ,related_name ='options')
    text =models .CharField (max_length =255 )

    def __str__ (self ):
        return self .text 

    def vote_count (self ):
        return self .votes .count ()


class PollVote (models .Model ):
    poll =models .ForeignKey (Poll ,on_delete =models .CASCADE ,related_name ='votes')
    option =models .ForeignKey (PollOption ,on_delete =models .CASCADE ,related_name ='votes')
    user =models .ForeignKey ('auth.User',on_delete =models .CASCADE ,related_name ='poll_votes')

    class Meta :
        unique_together =('poll','user')
