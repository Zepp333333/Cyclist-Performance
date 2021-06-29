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

class SummaryPRSegmentEffort(object):
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
        'pr_activity_id': 'int',
        'pr_elapsed_time': 'int',
        'pr_date': 'datetime',
        'effort_count': 'int'
    }

    attribute_map = {
        'pr_activity_id': 'pr_activity_id',
        'pr_elapsed_time': 'pr_elapsed_time',
        'pr_date': 'pr_date',
        'effort_count': 'effort_count'
    }

    def __init__(self, pr_activity_id=None, pr_elapsed_time=None, pr_date=None, effort_count=None):  # noqa: E501
        """SummaryPRSegmentEffort - a model defined in Swagger"""  # noqa: E501
        self._pr_activity_id = None
        self._pr_elapsed_time = None
        self._pr_date = None
        self._effort_count = None
        self.discriminator = None
        if pr_activity_id is not None:
            self.pr_activity_id = pr_activity_id
        if pr_elapsed_time is not None:
            self.pr_elapsed_time = pr_elapsed_time
        if pr_date is not None:
            self.pr_date = pr_date
        if effort_count is not None:
            self.effort_count = effort_count

    @property
    def pr_activity_id(self):
        """Gets the pr_activity_id of this SummaryPRSegmentEffort.  # noqa: E501

        The unique identifier of the activity related to the PR effort.  # noqa: E501

        :return: The pr_activity_id of this SummaryPRSegmentEffort.  # noqa: E501
        :rtype: int
        """
        return self._pr_activity_id

    @pr_activity_id.setter
    def pr_activity_id(self, pr_activity_id):
        """Sets the pr_activity_id of this SummaryPRSegmentEffort.

        The unique identifier of the activity related to the PR effort.  # noqa: E501

        :param pr_activity_id: The pr_activity_id of this SummaryPRSegmentEffort.  # noqa: E501
        :type: int
        """

        self._pr_activity_id = pr_activity_id

    @property
    def pr_elapsed_time(self):
        """Gets the pr_elapsed_time of this SummaryPRSegmentEffort.  # noqa: E501

        The elapsed time ot the PR effort.  # noqa: E501

        :return: The pr_elapsed_time of this SummaryPRSegmentEffort.  # noqa: E501
        :rtype: int
        """
        return self._pr_elapsed_time

    @pr_elapsed_time.setter
    def pr_elapsed_time(self, pr_elapsed_time):
        """Sets the pr_elapsed_time of this SummaryPRSegmentEffort.

        The elapsed time ot the PR effort.  # noqa: E501

        :param pr_elapsed_time: The pr_elapsed_time of this SummaryPRSegmentEffort.  # noqa: E501
        :type: int
        """

        self._pr_elapsed_time = pr_elapsed_time

    @property
    def pr_date(self):
        """Gets the pr_date of this SummaryPRSegmentEffort.  # noqa: E501

        The time at which the PR effort was started.  # noqa: E501

        :return: The pr_date of this SummaryPRSegmentEffort.  # noqa: E501
        :rtype: datetime
        """
        return self._pr_date

    @pr_date.setter
    def pr_date(self, pr_date):
        """Sets the pr_date of this SummaryPRSegmentEffort.

        The time at which the PR effort was started.  # noqa: E501

        :param pr_date: The pr_date of this SummaryPRSegmentEffort.  # noqa: E501
        :type: datetime
        """

        self._pr_date = pr_date

    @property
    def effort_count(self):
        """Gets the effort_count of this SummaryPRSegmentEffort.  # noqa: E501

        Number of efforts by the authenticated athlete on this segment.  # noqa: E501

        :return: The effort_count of this SummaryPRSegmentEffort.  # noqa: E501
        :rtype: int
        """
        return self._effort_count

    @effort_count.setter
    def effort_count(self, effort_count):
        """Sets the effort_count of this SummaryPRSegmentEffort.

        Number of efforts by the authenticated athlete on this segment.  # noqa: E501

        :param effort_count: The effort_count of this SummaryPRSegmentEffort.  # noqa: E501
        :type: int
        """

        self._effort_count = effort_count

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
        if issubclass(SummaryPRSegmentEffort, dict):
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
        if not isinstance(other, SummaryPRSegmentEffort):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
