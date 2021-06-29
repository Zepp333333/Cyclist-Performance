# coding: utf-8

"""
    Strava API v3

    The [Swagger Playground](https://developers.strava.com/playground) is the easiest way to familiarize yourself with the Strava API by submitting HTTP requests and observing the responses before you write any client code. It will show what a response will look like with different endpoints depending on the authorization scope you receive from your athletes. To use the Playground, go to https://www.strava.com/settings/api and change your “Authorization Callback Domain” to developers.strava.com. Please note, we only support Swagger 2.0. There is a known issue where you can only select one scope at a time. For more information, please check the section “client code” at https://developers.strava.com/docs.  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pprint
import re  # noqa: F401

import six

class PhotosSummaryPrimary(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'source': 'int',
        'unique_id': 'str',
        'urls': 'dict(str, str)'
    }

    attribute_map = {
        'id': 'id',
        'source': 'source',
        'unique_id': 'unique_id',
        'urls': 'urls'
    }

    def __init__(self, id=None, source=None, unique_id=None, urls=None):  # noqa: E501
        """PhotosSummaryPrimary - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._source = None
        self._unique_id = None
        self._urls = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if source is not None:
            self.source = source
        if unique_id is not None:
            self.unique_id = unique_id
        if urls is not None:
            self.urls = urls

    @property
    def id(self):
        """Gets the id of this PhotosSummaryPrimary.  # noqa: E501


        :return: The id of this PhotosSummaryPrimary.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PhotosSummaryPrimary.


        :param id: The id of this PhotosSummaryPrimary.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def source(self):
        """Gets the source of this PhotosSummaryPrimary.  # noqa: E501


        :return: The source of this PhotosSummaryPrimary.  # noqa: E501
        :rtype: int
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this PhotosSummaryPrimary.


        :param source: The source of this PhotosSummaryPrimary.  # noqa: E501
        :type: int
        """

        self._source = source

    @property
    def unique_id(self):
        """Gets the unique_id of this PhotosSummaryPrimary.  # noqa: E501


        :return: The unique_id of this PhotosSummaryPrimary.  # noqa: E501
        :rtype: str
        """
        return self._unique_id

    @unique_id.setter
    def unique_id(self, unique_id):
        """Sets the unique_id of this PhotosSummaryPrimary.


        :param unique_id: The unique_id of this PhotosSummaryPrimary.  # noqa: E501
        :type: str
        """

        self._unique_id = unique_id

    @property
    def urls(self):
        """Gets the urls of this PhotosSummaryPrimary.  # noqa: E501


        :return: The urls of this PhotosSummaryPrimary.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._urls

    @urls.setter
    def urls(self, urls):
        """Sets the urls of this PhotosSummaryPrimary.


        :param urls: The urls of this PhotosSummaryPrimary.  # noqa: E501
        :type: dict(str, str)
        """

        self._urls = urls

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(PhotosSummaryPrimary, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PhotosSummaryPrimary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
