properties([
    parameters([
        string(defaultValue: 'schema_quod', description: 'enter branch name which exists in th2-script-quod-demo repository', name: 'BranchName'),
        string(name: 'Name', defaultValue: 'Regression', description: ''),
        string(name: 'Version', defaultValue: '', description: 'e.g. 5.1.159.170'),
        separator(name: 'separator-323aceab-1ada-40c5-b7de-fd214cf067e0', sectionHeader: 'Choose mode'), 
        booleanParam('Regression'), 
        booleanParam('RunTestScript'),
        string(description: 'for example path/to/scirpt.py', name: 'TestScriptPath'),
        separator(name: 'separator-2708f255-81e3-46e7-915c-80eb4eb0aab2', sectionHeader: 'Algo product_line'), 
        booleanParam(defaultValue: true, name: 'algo'),
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Twap', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462400', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Vwap', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462401', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Participation', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462402', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Iceberg', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462403', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Multilisted', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462404', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Peg', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Stop', 
        omitValueField: true, 
        randomName: 'choice-parameter-163950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Lit_dark', 
        omitValueField: true, 
        randomName: 'choice-parameter-153950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Block', 
        omitValueField: true, 
        randomName: 'choice-parameter-143950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Gating_rules', 
        omitValueField: true, 
        randomName: 'choice-parameter-133950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Web_admin', 
        omitValueField: true, 
        randomName: 'choice-parameter-123950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mp_dark', 
        omitValueField: true, 
        randomName: 'choice-parameter-113950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Synth_min_qty', 
        omitValueField: true, 
        randomName: 'choice-parameter-103950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Lit_dark_iceberg', 
        omitValueField: true, 
        randomName: 'choice-parameter-93950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Sorping', 
        omitValueField: true, 
        randomName: 'choice-parameter-83950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Multiple_emulation', 
        omitValueField: true, 
        randomName: 'choice-parameter-73950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'PreOpen_Auction', 
        omitValueField: true, 
        randomName: 'choice-parameter-63950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Expity_Auction', 
        omitValueField: true, 
        randomName: 'choice-parameter-53950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'PreClose_Auction', 
        omitValueField: true, 
        randomName: 'choice-parameter-43950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Scaling', 
        omitValueField: true, 
        randomName: 'choice-parameter-033950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'POV_Scaling', 
        omitValueField: true, 
        randomName: 'choice-parameter-23950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Pair_trading', 
        omitValueField: true, 
        randomName: 'choice-parameter-13950261122462405', 
        referencedParameters: 'algo', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${algo ? 'checked' : ''}/>
                    """''']
            ]
        ],

        separator(name: 'separator-forex', sectionHeader: 'Forex product_line'),

        booleanParam(defaultValue: true, name: 'fx'),
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'ESP_MM', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462406', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'ESP_Taker', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462407', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'RFQ_MM', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462408', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'RFQ_Taker', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462409', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Position', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462410', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'AutoHedger', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462411', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Synthetic', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462412', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'FX_Acceptance_list', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462413', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'FX_Smoke_list', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462414', 
        referencedParameters: 'fx', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${fx ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],

        separator(name: 'separator-oms', sectionHeader: 'OMS product_line'),

        booleanParam(defaultValue: true, name: 'oms'),
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'DMA', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462415', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Care', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462416', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'BasketTrading', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462417', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Bag', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462418', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Positions', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462419', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'PostTrade', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462420', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Commissions', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462421', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'FETrading_Displaying', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462422', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Counterparts', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462423', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'ArchiveWindows', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462424', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Benchmark', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462425', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Dashboard', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462426', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Gateway', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462427', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'MDA', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462428', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'MarketDepth', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462429', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Piloting', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462430', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WatchList', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462431', 
        referencedParameters: 'oms', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${oms ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],

        separator(name: 'separator-retail', sectionHeader: 'Retail product_line'),
        booleanParam(defaultValue: true, name: 'retail'),
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'PRET_FETrading_Display', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462432', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'PRET_Position_Validity', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462433', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mobile_LoginLogout', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462434', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mobile_Account', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462435', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mobile_Market', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462436', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mobile_Others', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462437', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mobile_Portfolio', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462438', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Mobile_OrderTicket_OrderBook', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462439', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_Login_Logout', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462440', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_OrderTicket_Book', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462441', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_Other', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462442', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_Positions', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462443', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_Trades', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462444', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_UserProfile', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462445', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_WatchList', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462446', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WebTrading_AccountSummary', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462447', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Trading_REST_API_Dma', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462448', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Trading_REST_API_MarketData', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462449', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Trading_REST_API_Positions', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462450', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Trading_REST_API_RiskLimits', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462451', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Trading_REST_API_BuyingPower', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462452', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'Trading_REST_API_Others', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462453', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_REST_API_Site', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462454', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_REST_API_Users', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462455', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_REST_API_Client_Accounts', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462456', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_REST_API_Risk_Limits', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462457', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_REST_API_Positions', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462458', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_REST_API_Others', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462459', 
        referencedParameters: 'retail', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${retail ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        separator(name: 'separator-web_admin', sectionHeader: 'Web_admin product_line'),
        booleanParam(defaultValue: true, name: 'web_admin'),
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Client_Accounts', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462460', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_General', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462461', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Market_Making', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462462', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Middle_Office', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462463', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Order_Management', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462464', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Others', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462465', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Positions', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462466', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Reference_Data', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462467', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Risk_Limits', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462468', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Site', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462469', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ],
        [$class: 'DynamicReferenceParameter', 
        choiceType: 'ET_FORMATTED_HTML', 
        name: 'WA_Users', 
        omitValueField: true, 
        randomName: 'choice-parameter-33950261122462470', 
        referencedParameters: 'web_admin', 
        script: 
            [$class: 'GroovyScript', 
            fallbackScript: [classpath: [], sandbox: false, script: ''], script: [classpath: [], sandbox: false, 
                script: '''"""
                    <input type="checkbox" name="value"${web_admin ? \' checked\' : \'\'}/>
                    """''']
            ]
        ]
        ])
    ])
pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'  
        }
    }
    environment {
        REGRESSION_CONFIG = "${env.WORKSPACE}/regression_run_config.xml"
    }

    stages {
        stage('Algo section') {
            steps {
                sh '''
                    echo "Replacing params in XML config for algo product line"
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo'][@run]/@run" -v "${algo}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Twap'][@run]/@run" -v "${Twap}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Vwap'][@run]/@run" -v "${Vwap}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Participation'][@run]/@run" -v "${Participation}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Iceberg'][@run]/@run" -v "${Iceberg}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Multilisted'][@run]/@run" -v "${Multilisted}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Peg'][@run]/@run" -v "${Peg}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Stop'][@run]/@run" -v "${Stop}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Lit_dark'][@run]/@run" -v "${Lit_dark}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Block'][@run]/@run" -v "${Block}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Gating_rules'][@run]/@run" -v "${Gating_rules}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Web_admin'][@run]/@run" -v "${Web_admin}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Mp_dark'][@run]/@run" -v "${Mp_dark}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Synth_min_qty'][@run]/@run" -v "${Synth_min_qty}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Lit_dark_iceberg'][@run]/@run" -v "${Lit_dark_iceberg}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Sorping'][@run]/@run" -v "${Sorping}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Multiple_emulation'][@run]/@run" -v "${Multiple_emulation}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='PreOpen_Auction'][@run]/@run" -v "${PreOpen_Auction}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Expity_Auction'][@run]/@run" -v "${Expity_Auction}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='PreClose_Auction'][@run]/@run" -v "${PreClose_Auction}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Scaling'][@run]/@run" -v "${Scaling}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='POV_Scaling'][@run]/@run" -v "${POV_Scaling}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='algo']/components/component[@name='Pair_trading'][@run]/@run" -v "${Pair_trading}" ${REGRESSION_CONFIG}
                '''
            }
        }
        stage('Forex section') {
            steps {
                sh '''
                    echo "Replacing params in XML config for forex product line"
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx'][@run]/@run" -v "${fx}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='ESP_MM'][@run]/@run" -v "${ESP_MM}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='ESP_Taker'][@run]/@run" -v "${ESP_Taker}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='RFQ_MM'][@run]/@run" -v "${RFQ_MM}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='RFQ_Taker'][@run]/@run" -v "${RFQ_Taker}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='Position'][@run]/@run" -v "${Position}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='AutoHedger'][@run]/@run" -v "${AutoHedger}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='Synthetic'][@run]/@run" -v "${Synthetic}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='FX_Acceptance_list'][@run]/@run" -v "${FX_Acceptance_list}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='fx']/components/component[@name='FX_Smoke_list'][@run]/@run" -v "${FX_Smoke_list}" ${REGRESSION_CONFIG}
                '''
            }
        }
        stage('OMS section') {
            steps {
                sh '''
                    echo "Replacing params in XML config for oms product line"
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms'][@run]/@run" -v "${oms}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='DMA'][@run]/@run" -v "${DMA}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Care'][@run]/@run" -v "${Care}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='BasketTrading'][@run]/@run" -v "${BasketTrading}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Bag'][@run]/@run" -v "${Bag}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Positions'][@run]/@run" -v "${Positions}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='PostTrade'][@run]/@run" -v "${PostTrade}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Commissions'][@run]/@run" -v "${Commissions}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='FETrading_Displaying'][@run]/@run" -v "${FETrading_Displaying}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='ArchiveWindows'][@run]/@run" -v "${ArchiveWindows}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Benchmark'][@run]/@run" -v "${Benchmark}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Dashboard'][@run]/@run" -v "${Dashboard}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Gateway'][@run]/@run" -v "${Gateway}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='MDA'][@run]/@run" -v "${MDA}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='MarketDepth'][@run]/@run" -v "${MarketDepth}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='Piloting'][@run]/@run" -v "${Piloting}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='oms']/components/component[@name='WatchList'][@run]/@run" -v "${WatchList}" ${REGRESSION_CONFIG}
                '''
            }
        }
        stage('Retail section') {
            steps {
                sh '''
                    echo "Replacing params in XML config for retail product line"
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail'][@run]/@run" -v "${retail}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='PRET_FETrading_Display'][@run]/@run" -v "${PRET_FETrading_Display}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='PRET_Position_Validity'][@run]/@run" -v "${PRET_Position_Validity}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Mobile_LoginLogout'][@run]/@run" -v "${Mobile_LoginLogout}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Mobile_Account'][@run]/@run" -v "${Mobile_Account}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Mobile_Market'][@run]/@run" -v "${Mobile_Market}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Mobile_Others'][@run]/@run" -v "${Mobile_Others}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Mobile_Portfolio'][@run]/@run" -v "${Mobile_Portfolio}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Mobile_OrderTicket_OrderBook'][@run]/@run" -v "${Mobile_OrderTicket_OrderBook}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_Login_Logout'][@run]/@run" -v "${WebTrading_Login_Logout}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_OrderTicket_Book'][@run]/@run" -v "${WebTrading_OrderTicket_Book}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_Other'][@run]/@run" -v "${WebTrading_Other}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_Positions'][@run]/@run" -v "${WebTrading_Positions}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_Trades'][@run]/@run" -v "${WebTrading_Trades}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_UserProfile'][@run]/@run" -v "${WebTrading_UserProfile}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_WatchList'][@run]/@run" -v "${WebTrading_WatchList}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WebTrading_AccountSummary'][@run]/@run" -v "${WebTrading_AccountSummary}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Trading_REST_API_Dma'][@run]/@run" -v "${Trading_REST_API_Dma}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Trading_REST_API_MarketData'][@run]/@run" -v "${Trading_REST_API_MarketData}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Trading_REST_API_Positions'][@run]/@run" -v "${Trading_REST_API_Positions}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Trading_REST_API_RiskLimits'][@run]/@run" -v "${Trading_REST_API_RiskLimits}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Trading_REST_API_BuyingPower'][@run]/@run" -v "${Trading_REST_API_BuyingPower}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='Trading_REST_API_Others'][@run]/@run" -v "${Trading_REST_API_Others}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WA_REST_API_Site'][@run]/@run" -v "${WA_REST_API_Site}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WA_REST_API_Users'][@run]/@run" -v "${WA_REST_API_Users}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WA_REST_API_Client_Accounts'][@run]/@run" -v "${WA_REST_API_Client_Accounts}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WA_REST_API_Risk_Limits'][@run]/@run" -v "${WA_REST_API_Risk_Limits}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WA_REST_API_Positions'][@run]/@run" -v "${WA_REST_API_Positions}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='retail']/components/component[@name='WA_REST_API_Others'][@run]/@run" -v "${WA_REST_API_Others}" ${REGRESSION_CONFIG}
                '''
            }
        }
        stage('Web_admin section') {
            steps {
                sh '''
                    echo "Replacing params in XML config for Web_admin product line"
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin'][@run]/@run" -v "${web_admin}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Client_Accounts'][@run]/@run" -v "${WA_Client_Accounts}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_General'][@run]/@run" -v "${WA_General}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Market_Making'][@run]/@run" -v "${WA_Market_Making}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Middle_Office'][@run]/@run" -v "${WA_Middle_Office}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Order_Management'][@run]/@run" -v "${WA_Order_Management}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Others'][@run]/@run" -v "${WA_Others}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Positions'][@run]/@run" -v "${WA_Positions}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Reference_Data'][@run]/@run" -v "${WA_Reference_Data}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Risk_Limits'][@run]/@run" -v "${WA_Risk_Limits}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Site'][@run]/@run" -v "${WA_Site}" ${REGRESSION_CONFIG}
                    xmlstarlet ed -L -u "/regression/product_lines/product_line[@name='web_admin']/components/component[@name='WA_Users'][@run]/@run" -v "${WA_Users}" ${REGRESSION_CONFIG}
                '''
            }
        }
        stage('Additional changes to config') {
            steps {
                sh '''
                xmlstarlet ed -L -u "/regression/name" -v "${Name}" ${REGRESSION_CONFIG}
                xmlstarlet ed -L -u "/regression/version" -v "${Version}" ${REGRESSION_CONFIG}
                sed -i 's|false|False|g' ${REGRESSION_CONFIG}
                sed -i 's|true|True|g' ${REGRESSION_CONFIG} 
                '''
            }
        }
        stage('Regression') {
            when {
                expression { return params.Regression }
            }
            steps {
                sh '''
                    echo "Regression stage"
                    export PATH=$PATH:$WORKSPACE/.local/bin/ && \\
                    export HOME=$WORKSPACE && \\
                    cat /var/th2/config/log_config.conf && \\
                    pip install psycopg2-binary --user && \\
                    pip install -r requirements.txt --user && \\
                    python3 regression_run.py --user
                '''
            }
        }
        stage('Run test script') {
            when {
                expression { return params.RunTestScript }
            }
            steps {
                sh '''
                    echo "Run test script stage"
                    export PATH=$PATH:$WORKSPACE/.local/bin/ && \\
                    export PYTHONPATH=/release/jenkins-loki/workspace/qa-tests.pipeline/ && \\
                    export HOME=$WORKSPACE && \\
                    cat /var/th2/config/log_config.conf && \\
                    pip install psycopg2-binary --user && \\
                    pip install -r requirements.txt --user && \\
                    python3 ${TestScriptPath} --user
                '''
            }
        }
    }

    post {
        cleanup {
            deleteDir()
        }        
    }
}