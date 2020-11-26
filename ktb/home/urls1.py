from django.urls import path
from django.conf.urls import url,include
from home import views

app_name='home'

urlpatterns = [
    url(r'^$',views.UserLogin,name='userlogin'),
    url(r'^index',views.Index,name='index'),
    url(r'^dash',views.Dashboard,name='dashboard'),
    url(r'^users/',views.Users,name='users'),
    url(r'^saveusers/',views.SaveUsers,name='saveUsers'),
    url(r'^kyc/',views.KycData,name='kyc'),
    url(r'^tradeapproval/',views.TradeApprove,name='tradeApproval'),
    url(r'^tradeapprove/',views.Approve,name='approveTrade'),
    url(r'^tradesave/',views.SaveApproval,name='save'),
    url(r'^tradeapproved/',views.TradeApproved,name='tradeApproved'),
    url(r'^predocuments/',views.PreDocuments,name='preDocuments'),
    url(r'^prepayments/',views.Prepayments,name='prepayments'),
    url(r'^prepaymenthelper/',views.PrepaymentsHelper,name='prepaymentsHelper'),
    url(r'^saveprepay/',views.SavePayments,name='savepre'),
    url(r'^salespurchase/',views.SalesPurchase,name='salesPurchase'),
    url(r'^savesalespurchase/',views.SaveSalesPurchase,name='saveSalesPurchase'),
    url(r'^salespurchasehelper/',views.SalesPurchaseHelper,name='helperSalesPurchase'),

    url(r'^extras/',views.ExtraCosts,name='extraCost'),
    url(r'^saveextras/',views.SaveExtraCost,name='saveExtras'),
    url(r'^finance/',views.PaymentFinance,name='paymentFinance'),
    url(r'^savefinance/',views.SaveFinance,name='savepaymentFinance'),
    url(r'^financehelper/',views.PaymentFinanceHelper,name='helperpaymentFinance'),
    url(r'^disputes/',views.Dispute,name='disputes'),
    url(r'^savedisputes/',views.SaveDisputes,name='savedispute'),
    url(r'^pl/',views.PLBook,name='pl'),
    url(r'^plsave/',views.SavePLBook,name='savepl'),
    url(r'^inventory/',views.Inventory,name='inventory'),
    url(r'^stocks/',views.Stock,name='stocks'),
    url(r'^savestocks/',views.SaveStock,name='savestocks'),
    url(r'^savekyc/',views.SaveKyc,name='savekyc'),
    url(r'^editkyc/',views.EditKyc,name='editkyc'),
    url(r'^fetchcompany/',views.FetchCompany,name='fetchComp'),
    url(r'^getdata1/',views.GetDataSales,name='getsales'),
    url(r'^getdata2/',views.GetDataPurchase,name='getpurchase'),
    url(r'^getdata/',views.GetDataInventory,name='getInventoryData'),
    url(r'^savedata/',views.SaveInventoryRecord,name='saveInventoryData'),
    url(r'^data/',views.GetProduct,name='getProductData'),
    url(r'^log/',views.LogFile,name='log'),

    url(r'^trace/',views.GetProductTrace,name='getproducttrace'),
    url(r'^getextra/',views.ExtrasHelper,name='extrashelper'),


#new --------------------------------------
    url(r'^payablemore/',views.PayableMore, name='getpayablemore'),
    url(r'^receivablemore/',views.ReceivableMore, name='getreceivablemore'),
    url(r'^bar/',views.GetPieData, name='getpiedata'),
    url(r'^salesbill/',views.GetSalesBill, name='getsalesbill'),

    url(r'^getstockproduct/',views.GetStockProduct, name='getStockProduct'),

    # ---------------------edit-------------------------------
    url(r'^editapproval/',views.EditTradeApproval,name='editTradeApproval'),
    url(r'^editapproved/',views.EditTradeApproved,name='editTradeApproved'),
    url(r'^editdoc/',views.EditDoc,name='editTradeDoc'),
    url(r'^editprepay/',views.EditPrePayments,name='editPrePayments'),
    url(r'^salespurchaseedit/',views.EditSalesAndPurchase,name='editSalesPurchase'),
    url(r'^editextras/',views.EditExtras,name='editExtras'),
    url(r'^editfinance/',views.EditPurchaseAndFinance,name='editFinance'),
    url(r'^editDisputes/',views.EditDisputes,name='editDisputes'),
    url(r'^editinventory/',views.EditInventory,name='editInventory'),
    url(r'^editstock/',views.EditStock,name='editStock'),
    url(r'^edituser/',views.EditUsers,name='edituser'),
     # editpl
    url(r'^editpl/',views.EditPL,name='editPL'),
# alter value -----------------------
    url(r'^alterapproval/',views.AlterTradeApproval,name='alterTradeApproval'),
    url(r'^alterapproved/',views.AlterTradeApproved,name='alterTradeApproved'),
    url(r'^alterprepay/',views.AlterPrePayments,name='alterPrePayments'),
    url(r'^altersalespurchase/',views.AlterSalesPurchase,name='alterSalesPurchase'),
    url(r'^alterextras/',views.AlterExtras,name='alterExtras'),
    url(r'^alterfinance/',views.AlterFinance,name='alterFinance'),
    url(r'^alterstock/',views.AlterStock,name='alterStock'),
    url(r'^alterkyc/',views.AlterKyc,name='alterKyc'),
    url(r'^delkyc/',views.DelKyc,name='delKyc'),
    url(r'^alteruser/',views.AlterUser,name='alteruser'),
    url(r'^deluser/',views.DelUser,name='delUser'),
    url(r'^alterpl/',views.AlterPL,name='alterPL'),
    url(r'^amend/',views.AmendValues,name='amendValues'),
    url(r'^deletestock/',views.DeleteStockJournal,name='deleteStockJournal'),

    #filters ....................................................................
    url(r'^filterapproval/',views.GetTradeApproval,name='gettradeapproval'),
    url(r'^filterapproved/',views.GetTradeApproved,name='gettradeapproved'),
    url(r'^filterpre/',views.GetPresale,name='getpresale'),
    url(r'^filterprepay/',views.GetPrepayment,name='getprepayment'),
    url(r'^filtersalespurchase/',views.GetSalesPurchase,name='getsalespurchase'),
    url(r'^filterextra/',views.GetExtras,name='getextras'),
    url(r'^filterfinance/',views.GetFinance,name='getfinance'),

    url(r'^qtygetapproved/',views.GetQtyApprovedDetailPurchase,name='qtyapproveddetailpurchase'),
    url(r'^qtygetapprovedsale/',views.GetQtyApprovedDetailSales,name='qtyapproveddetailsales'),
    url(r'^qtygetapprovedhelp/',views.GetQtyApprovedDetailPurchaseHelper,name='qtyapproveddetailpurchasehelper'),
    url(r'^qtygetapprovedsalehelp/',views.GetQtyApprovedDetailSalesHelper,name='qtyapproveddetailsaleshelper'),

    url(r'^filterpl/',views.FilterPL,name='filterp&l'),
    url(r'^filterp/',views.FilterP,name='filterpurchase'),
    url(r'^filters/',views.FilterS,name='filtersales'),
    # qtyapproveddetail

    url(r'^financedate/',views.FinanceDate,name='financeDate'),
    url(r'^spdate/',views.SPDate,name='spDate'),
    url(r'^approvedfilter/',views.ApprovedFilter,name='filterapproved'),
    url(r'^approvesp/',views.ApproveSP,name='approveSalesPurchase'),


      #--------------------excels-------------------------------------------------------
    url(r'^exportapproval/(?P<approval>\w*)/',views.ExportApproval,name='exportApproval'),
    url(r'^exportapproved/(?P<approved>\w*)/',views.ExportApproved,name='exportApproved'),
    url(r'^exportapprovedfilter/(?P<year>\w*)/(?P<month>\w*)/',views.ExportApprovedFilter,name='exportApprovedFilter'),
    url(r'^exportdoc/',views.ExportDoc,name='exportDoc'),
    url(r'^exportpre/',views.ExportPre,name='exportPrepayment'),
    url(r'^exportsp/',views.ExportSP,name='exportSalesPurchase'),
    url(r'^exportextras/',views.ExportExtras,name='exportExtras'),
    url(r'^exportfinance/(?P<approval>\w*)/',views.ExportFinance,name='exportFinance'),
    url(r'^exportfinancefilter/(?P<year>\w*)/(?P<month>\w*)/',views.ExportFinanceFilter,name='exportFinanceFilter'),
    url(r'^exportprofit/',views.ExportProfit,name='exportProfit'),
    url(r'^exportfilterprofit/(?P<year>\w*)/(?P<month>\w*)/',views.ExportFilterProfit,name='exportFilterProfit'),
    url(r'^exportkyc/',views.ExportKyc,name='exportKyc'),
    url(r'^exportsales/',views.ExportSales,name='exportSales'),
    url(r'^exportsalesfilter/(?P<year>\w*)/(?P<month>\w*)/',views.ExportSalesFilter,name='exportSalesFilter'),
    url(r'^exportpurchase/',views.ExportPurchase,name='exportPurchase'),
    url(r'^exportpurchasefilter/(?P<year>\w*)/(?P<month>\w*)/',views.ExportPurchaseFilter,name='exportPurchaseFilter'),
    url(r'^exportinv/',views.ExportInventory,name='exportInventory'),


    # kyc approval
    url(r'^approvekyc1/',views.ApproveKyc1,name='approveKyc1'),
    url(r'^approvekyc2/',views.ApproveKyc2,name='approveKyc2'),
    
    # url(r'^dashexportfinance/',views.ExportDashFinance,name='dueFinanceExport'),
    url(r'^checkfiance/',views.CheckFinance,name='checkfinance'),
    # url(r'^dashexportpre/',views.ExportDashPre,name='duePreExport'),)
    url(r'^checkpre/',views.CheckPre,name='checkpre'),
# delete------------------------------------------------------------------------------
    url(r'^delapproval/',views.DelApproval,name='delApproval'),
    url(r'^delapproved/',views.DelApproved,name='delApproved'),
    url(r'^delpre/',views.DelPrepayment,name='delPrepayment'),
    url(r'^delsp/',views.DelSP,name='delSP'),
    url(r'^delextra/',views.DelExtra,name='delExtra'),
    url(r'^delfinance/',views.DelFinance,name='delFinance'),
    url(r'^delpnl/',views.DelPnL,name='delPl'),

    url(r'^getrate',views.GetRate,name='get_rate'),
]
