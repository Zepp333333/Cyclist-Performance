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

class Zones(object):
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
        'heart_rate': 'HeartRateZoneRanges',
        'power': 'PowerZoneRanges'
    }

    attribute_map = {
        'heart_rate': 'heart_rate',
        'power': 'power'
    }

    def __init__(self, heart_rate=None, power=None):  # noqa: E501
        """Zones - a model defined in Swagger"""  # noqa: E501
        self._heart_rate = None
        self._power = None
        self.discriminator = None
        if heart_rate is not None:
            self.heart_rate = heart_rate
        if power is not None:
            self.power = power

    @property
    def heart_rate(self):
        """Gets the heart_rate of this Zones.  # noqa: E501


        :return: The heart_rate of this Zones.  # noqa: E501
        :rtype: HeartRateZoneRanges
        """
        return self._heart_rate

    @heart_rate.setter
    def heart_rate(self, heart_rate):
        """Sets the heart_rate of this Zones.


        :param heart_rate: The heart_rate of this Zones.  # noqa: E501
        :type: HeartRateZoneRanges
        """

        self._heart_rate = heart_rate

    @property
    def power(self):
        """Gets the power of this Zones.  # noqa: E501


        :return: The power of this Zones.  # noqa: E501
        :rtype: PowerZoneRanges
        """
        return self._power

    @power.setter
    def power(self, power):
        """Sets the power of this Zones.


        :param power: The power of this Zones.  # noqa: E501
        :type: PowerZoneRanges
        """

        self._power = power

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
        if issubclass(Zones, dict):
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
        if not isinstance(other, Zones):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
