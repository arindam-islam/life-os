#!/usr/bin/env python3
import plistlib
import os

os.makedirs('/Users/ari/Documents/life-os/portal/shortcuts', exist_ok=True)
output_path = '/Users/ari/Documents/life-os/portal/shortcuts/Life_OS_Capture.shortcut'

shortcut_dict = {
    'WFWorkflowClientVersion': '2607.1',
    'WFWorkflowClientRelease': '3.0',
    'WFWorkflowMinimumClientVersion': 900,
    'WFWorkflowIcon': {
        'WFWorkflowIconGlyphNumber': 59771,
        'WFWorkflowIconStartColor': 431817727
    },
    'WFWorkflowTypes': ['ActionExtension'],
    'WFWorkflowInputContentItemClasses': [
        'WFURLContentItem',
        'WFStringContentItem',
        'WFImageContentItem'
    ],
    'WFWorkflowActions': [
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.geturls',
            'WFWorkflowActionParameters': {
                'WFInput': {
                    'Value': {
                        'Type': 'ExtensionInput'
                    },
                    'WFSerializationType': 'WFTextTokenAttachment'
                }
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.downloadurl',
            'WFWorkflowActionParameters': {
                'WFURL': 'https://arindamislam.duckdns.org/webhook/life-os/slack-inbox',
                'WFHTTPMethod': 'POST',
                'WFHTTPHeaders': {
                    'Value': {
                        'WFHTTPHeaders': [
                            {'WFHTTPHeaderField': 'Content-Type', 'WFHTTPHeaderValue': 'application/json'}
                        ]
                    },
                    'WFSerializationType': 'WFHTTPHeadersTableParameter'
                },
                'WFHTTPBodyType': 'JSON',
                'WFJSONValues': {
                    'Value': {
                        'WFDictionaryFieldValueItems': [
                            {
                                'WFItemType': 0,
                                'WFKey': {'Value': {'string': 'text'}, 'WFSerializationType': 'WFTextTokenString'},
                                'WFValue': {
                                    'Value': {
                                        'attachmentsByRange': {'{0, 1}': {'Type': 'ActionOutput', 'OutputName': 'URLs'}},
                                        'string': '\ufffc'
                                    },
                                    'WFSerializationType': 'WFTextTokenString'
                                }
                            },
                            {
                                'WFItemType': 0,
                                'WFKey': {'Value': {'string': 'channel'}, 'WFSerializationType': 'WFTextTokenString'},
                                'WFValue': {'Value': {'string': 'C0BPQBNTK8R'}, 'WFSerializationType': 'WFTextTokenString'}
                            }
                        ]
                    },
                    'WFSerializationType': 'WFDictionaryFieldValue'
                }
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getitemfromlist',
            'WFWorkflowActionParameters': {
                'WFItemSpecifier': 'First Item',
                'WFInput': {
                    'Value': {
                        'OutputName': 'Contents of URL',
                        'Type': 'ActionOutput'
                    },
                    'WFSerializationType': 'WFTextTokenAttachment'
                }
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getvalueforkey',
            'WFWorkflowActionParameters': {
                'WFDictionaryKey': 'status',
                'WFInput': {
                    'Value': {
                        'OutputName': 'Item from List',
                        'Type': 'ActionOutput'
                    },
                    'WFSerializationType': 'WFTextTokenAttachment'
                }
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getvalueforkey',
            'WFWorkflowActionParameters': {
                'WFDictionaryKey': 'message',
                'WFInput': {
                    'Value': {
                        'OutputName': 'Item from List',
                        'Type': 'ActionOutput'
                    },
                    'WFSerializationType': 'WFTextTokenAttachment'
                }
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
            'WFWorkflowActionParameters': {
                'WFCondition': 4,
                'WFConditionalActionString': 'saved',
                'WFInput': {
                    'Value': {
                        'OutputName': 'Dictionary Value',
                        'Type': 'ActionOutput'
                    },
                    'WFSerializationType': 'WFTextTokenAttachment'
                }
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.notification',
            'WFWorkflowActionParameters': {
                'WFNotificationActionBody': {
                    'Value': {
                        'attachmentsByRange': {'{0, 1}': {'Type': 'ActionOutput', 'OutputName': 'Dictionary Value'}},
                        'string': '\ufffc'
                    },
                    'WFSerializationType': 'WFTextTokenString'
                },
                'WFNotificationActionTitle': '✓ Captured to Life OS'
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
            'WFWorkflowActionParameters': {
                'WFControlFlowMode': 1
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.notification',
            'WFWorkflowActionParameters': {
                'WFNotificationActionBody': '✕ Life OS capture was not saved',
                'WFNotificationActionTitle': 'Life OS Capture'
            }
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.conditional',
            'WFWorkflowActionParameters': {
                'WFControlFlowMode': 2
            }
        }
    ]
}

with open(output_path, 'wb') as f:
    plistlib.dump(shortcut_dict, f, fmt=plistlib.FMT_BINARY)

print(f"✅ Created binary shortcut plist: {output_path}")
