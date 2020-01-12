# kicad源码分析

### kicad spice 模拟器

    void SIM_PLOT_FRAME::StartSimulation()
        STRING_FORMATTER formatter; 保存输出的Netlist字符串
        updateNetlistExporter(); 创建一个NetlistExporter对象, 并从schama中更新Netlist对象
        m_exporter->Format(formatter); 导出Netlist字符串
            ProcessNetlist(); 处理网表
                m_netMap.clear();
                m_netMap["GND"] = 0; Maps circuit nodes to net names
                UpdateDirectives(); 更新spice指令
                    for sheetList:
                        for item EDA_ITEM*:
                            item不是SCH_TEXT_T类型, 则continue
                            取出item的text
                            以"\r\n"分离text, 得到line数组, 对每一项line转小写
                            如果 line startwith ".inc", 更新 m_libraries
                            如果 line startwith ".title", 更新 m_title
                            如果 line startwith ".control", endwith ".endc", 更新 m_directives
                            如果 line startwith ".", "+", 更新 m_directives
                for sheetList:
                    for item EDA_ITEM*:
                        findNextComponentAndCreatePinList():
                            finds a component from the DrawList and builds its pin list in m_SortedComponentPinList.
                        更新 m_libraries
                        更新 m_spiceItems
            aFormatter->Print: ".title" ".include" device node model directives ".end"



    当添加信号onAddSignal():
        DIALOG_SIGNAL_LIST dialog.ShowModal:
            DIALOG_SIGNAL_LIST::TransferDataToWindow():
                for net m_exporter->GetNetIndexMap(): // Voltage list
                    m_signals->Append --> netname != "GND" && netname != "0": "V(%s)".format(netname)
                for item m_exporter->GetSpiceItems():
                    for current NETLIST_EXPORTER_PSPICE_SIM::GetCurrents( item.m_primitive ):
                        m_signals->Append --> "%s(%s)".format(current, item.m_refName)


    当选择信号后 TransferDataFromWindow():

