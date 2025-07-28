# Rest framewrok
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Permissions
from rest_framework.permissions import AllowAny

# Models
from fpt.users.models import User

# Serializers
from .serializers import UserSerializer
from fpt.users.api.serializers import TransactionSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class TransactionViewSet(mixins.CreateModelMixin, GenericViewSet):
    """Receptor wompi transactions viewset."""

    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create Membership and return response to bank."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"response": "Thanks wompi."}
        return Response(data, status=status.HTTP_200_OK)
